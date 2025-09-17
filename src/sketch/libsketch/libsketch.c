#include <stdbool.h>
#include <math.h>

#define STB_DS_IMPLEMENTATION
#include <stb/stb_ds.h>
#define STB_IMAGE_IMPLEMENTATION
#include <stb/stb_image.h>
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include <stb/stb_image_resize.h>

#include <potracelib.h>

#include "libsketch.h"

// xochitl won't render a line consisting of more points
const int MAX_POINTS = 30000;
const int POINTS_CAP = 0.7 * MAX_POINTS;
const int POINT_SIZE = 14;

unsigned char sig_len(unsigned char val) { return val << 4 | 0x0C; }
unsigned char sig_id(unsigned char val) { return val << 4 | 0x0F; }
unsigned char sig_int(unsigned char val) { return val << 4 | 0x04; }
unsigned char sig_dbl(unsigned char val) { return val << 4 | 0x08; }

PacketHeader create_header() {
    return (PacketHeader){0, 0x00, 0x02, 0x02, LINE_PACKET};
}

LinePoints create_line(Point* points) {
    int sig_cnt = 1;
    LinePoints line = {
        .length_sig = sig_len(6), .length = 0,
        .unknown_byte = 0x03,
        .tool_sig = sig_int(sig_cnt++), .tool = TOOL_MECHANICAL,
        .color_sig = sig_int(sig_cnt++), .color = COLOR_BLACK,
        .thickness_scale_sig = sig_dbl(sig_cnt++), .thickness_scale = 1.0,
        .starting_length_sig = sig_int(sig_cnt++), .starting_length = 0,
        .points_length_sig = sig_len(sig_cnt++), .points_length = POINT_SIZE * arrlen(points),
        .points = points,
        .ts_sig = sig_id(sig_cnt++), .ts = NULL
    };
    encode_id(0, 1, &line.ts);
    line.length = 31 + arrlen(line.points) * POINT_SIZE + arrlen(line.ts);
    return line;
}

LinePacket create_packet(int layer_id_major, int layer_id_minor, int counter, Point* points) {
    int sig_cnt = 1;
    LinePacket packet = {
        .header = create_header(),
        .parent_id_sig = sig_id(sig_cnt++), .parent_id = NULL,
        .id_sig = sig_id(sig_cnt++), .id = NULL,
        .left_sig = sig_id(sig_cnt++), .left = NULL,
        .right_sig = sig_id(sig_cnt++), .right = NULL,
        .deleted_length_sig = sig_int(sig_cnt++), .deleted_length = 0,
        .line = create_line(points)
    };
    // if one of the parent ids in the packets doesn't match existing layer 
    // all layers in the document will dissapear (except template and text)
    encode_id(layer_id_major, layer_id_minor, &packet.parent_id);
    encode_id(1, counter, &packet.id);
    encode_id(0, 0, &packet.left);
    encode_id(0, 0, &packet.right);
    packet.header.length = 14 + packet.line.length + arrlen(packet.parent_id) + arrlen(packet.id) + arrlen(packet.left) + arrlen(packet.right);
    return packet;
}

void encode_leb128(int val, char** buf) {
    do {
        char byte = val & 0x7f;
        val >>= 7;
        if (val != 0) byte |= 0x80;
        arrpush(*buf, byte);
    } while (val != 0);
}

void encode_id(int major, int minor, char** buf) {
    encode_leb128(major, buf);
    encode_leb128(minor, buf);
}

Point new_point_with_shade(int translate_x, int translate_y, int x, int y, int val, int shades) {
    char pressure = 0xff * (1.0 - ((float)value_to_shade(val, shades)) / ((float)shades));
    return (Point){(float)(x + translate_x), (float)(y + translate_y), 4, 
        value_to_shade(val, shades) == shades - 1 ? 0 : 4, 
        0, pressure};
}

Point new_point_with_width(int translate_x, int translate_y, int x, int y, int width) {
    return (Point){(float)(x + translate_x), (float)(y + translate_y), 4, 
        width * 4, 
        0, 0xff};
}

int pixel_to_value(int val, int alpha) {
    if (alpha == 255)
        return val;
    else if (alpha == 0)
        return 255;
    return (int)(val + ((255 - val) * (1 - (alpha / 255.0))));
}

int value_to_shade(int val, int shades) {
    return (int)floor(val / 256.0 * shades);
}

int following_pixel_shade(stbi_uc* data, int following_x, int y, int shades, int width) {
    if (following_x < 0 || following_x == width) return -1;
    return value_to_shade(get_pixel(data, following_x, y, width), shades);
}

int get_pixel(stbi_uc* data, int x, int y, int width) {
    int i = (y*width + x) * 2;
    return pixel_to_value(data[i], data[i+1]);
}

stbi_uc* fit_image(stbi_uc* data, int page_width, int page_height, int margin, int *w, int *h) {
    int width = *w; int height = *h;
    if ((float)width / (float)height > (float)page_width / (float)page_height) {
        if (width > page_width) {
            stbi_uc* copy = data;
            int in_w = width;
            int in_h = height;
            height = height * page_width / (float)width;
            width = page_width;
            data = malloc(width * height * 2);
            stbir_resize_uint8(copy, in_w, in_h, 0,
                data, width, height, 0, 2);
            stbi_image_free(copy);
        }
    } else {
        if (height > page_height) {
            stbi_uc* copy = data;
            int in_w = width;
            int in_h = height;
            width = width * page_height / (float)height;
            height = page_height;
            data = malloc(width * height * 2);
            stbir_resize_uint8(copy, in_w, in_h, 0,
                data, width, height, 0, 2);
            stbi_image_free(copy);
        }
    }
    *w = width; *h = height;
    return data;
}

int infer_bezier_steps(potrace_dpoint_t a, potrace_dpoint_t u,
    potrace_dpoint_t w, potrace_dpoint_t b) {
    int au = ceil(sqrt(pow(a.x-u.x, 2) + pow(a.y-u.y, 2)));
    int uw = ceil(sqrt(pow(u.x-w.x, 2) + pow(u.y-w.y, 2)));
    int wb = ceil(sqrt(pow(w.x-b.x, 2) + pow(w.y-b.y, 2)));
    int ab = ceil(sqrt(pow(a.x-b.x, 2) + pow(a.y-b.y, 2)));
    return (int)ceil(sqrt(au + uw + wb - ab)) * 2 + 1;
}

size_t serialize_packet(LinePacket packet, char* dest) {
    size_t n = 0;
    memcpy(dest + n, &packet.header, 8); n += 8;
    memcpy(dest + n, &packet.parent_id_sig, 1); n += 1;
    memcpy(dest + n, packet.parent_id, arrlen(packet.parent_id)); n += arrlen(packet.parent_id);
    memcpy(dest + n, &packet.id_sig, 1); n += 1;
    memcpy(dest + n, packet.id, arrlen(packet.id)); n += arrlen(packet.id);
    memcpy(dest + n, &packet.left_sig, 1); n += 1;
    memcpy(dest + n, packet.left, arrlen(packet.left)); n += arrlen(packet.left);
    memcpy(dest + n, &packet.right_sig, 1); n += 1;
    memcpy(dest + n, packet.right, arrlen(packet.right)); n += arrlen(packet.right);
    memcpy(dest + n, &packet.deleted_length_sig, 1); n += 1;
    memcpy(dest + n, &packet.deleted_length, 4); n += 4;
    memcpy(dest + n, &packet.line.length_sig, 1); n += 1;
    memcpy(dest + n, &packet.line.length, 4); n += 4;
    memcpy(dest + n, &packet.line.unknown_byte, 1); n += 1;
    memcpy(dest + n, &packet.line.tool_sig, 1); n += 1;
    memcpy(dest + n, &packet.line.tool, 4); n += 4;
    memcpy(dest + n, &packet.line.color_sig, 1); n += 1;
    memcpy(dest + n, &packet.line.color, 4); n += 4;
    memcpy(dest + n, &packet.line.thickness_scale_sig, 1); n += 1;
    memcpy(dest + n, &packet.line.thickness_scale, 8); n += 8;
    memcpy(dest + n, &packet.line.starting_length_sig, 1); n += 1;
    memcpy(dest + n, &packet.line.starting_length, 4); n += 4;
    memcpy(dest + n, &packet.line.points_length_sig, 1); n += 1;
    memcpy(dest + n, &packet.line.points_length, 4); n += 4;
    memcpy(dest + n, packet.line.points, arrlen(packet.line.points) * POINT_SIZE); n += arrlen(packet.line.points) * POINT_SIZE;
    memcpy(dest + n, &packet.line.ts_sig, 1); n += 1;
    memcpy(dest + n, packet.line.ts, arrlen(packet.line.ts)); n += arrlen(packet.line.ts);
    return n;
}

size_t convert_naive(char* filename, int page_width, 
    int page_height, int margin, int layer_id_major, 
    int layer_id_minor, int shades, int *id_counter, char* buf) {
    size_t result = 0;

    int width = 0;
    int height = 0;
    int channels = 0;
    // channels bw & alpha
    stbi_uc* data = stbi_load(filename, &width, &height, &channels, 2);
    if (data == NULL) {
        return 0;
    }
    data = fit_image(data, page_width, page_height, margin, &width, &height);
    int translate_x = -width / 2.0;
    int translate_y = margin + (page_height - height) / 2.0;

    Point* points = NULL;
    int previous_shade = -1;
    bool left_to_right = true;
    for (int y = 0; y < height; y++) {
        if (left_to_right) {
            for (int x = 0; x < width; x++) {
                int val = get_pixel(data, x, y, width);
                int shade = value_to_shade(val, shades);
                if (previous_shade != shade || following_pixel_shade(
                        data, x+1, y, shades, width) != shade) {
                    previous_shade = shade;
                    arrpush(points, new_point_with_shade(translate_x, translate_y, x ,y, val, shades));
                }
            }
        } else {
            for (int x = width - 1; x >= 0; x--) {
                int val = get_pixel(data, x, y, width);
                int shade = value_to_shade(val, shades);
                if (previous_shade != shade || following_pixel_shade(
                        data, x-1, y, shades, width) != shade) {
                    previous_shade = shade;
                    arrpush(points, new_point_with_shade(translate_x, translate_y, x ,y, val, shades));
                }
            }
        }
        previous_shade = -1;
        left_to_right = !left_to_right;

        if (arrlen(points) >= POINTS_CAP) {
            result += serialize_packet(create_packet(layer_id_major, layer_id_minor, (*id_counter)++, points), buf + result);
            arrfree(points);
            points = NULL;
        }
    }
    stbi_image_free(data);

    if (arrlen(points) > 0) {
        result += serialize_packet(create_packet(layer_id_major, layer_id_minor, (*id_counter)++, points), buf + result);
        arrfree(points);
    }
    return result;
}

size_t convert_potrace(char* filename, int page_width, 
    int page_height, int margin, int layer_id_major, 
    int layer_id_minor, int threshold, int *id_counter, char* buf) {
    size_t result = 0;

    int width = 0;
    int height = 0;
    int channels = 0;
    // channels bw & alpha
    stbi_uc* data = stbi_load(filename, &width, &height, &channels, 2);
    if (data == NULL) {
        return 0;
    }
    data = fit_image(data, page_width, page_height, margin, &width, &height);
    int translate_x = -width / 2.0;
    int translate_y = margin + (page_height - height) / 2.0;

    unsigned long word_len = sizeof(potrace_word) * 8;
    potrace_bitmap_t bitmap;
    bitmap.w = width; bitmap.h = height;
    bitmap.dy = ceil(bitmap.w / (float)word_len); // len in words
    bitmap.map =  calloc(bitmap.dy * bitmap.h, sizeof(potrace_word));
    // convert stbi data to potrace bitmap
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            bitmap.map[y*bitmap.dy + x / word_len] |= 
                (unsigned long)(get_pixel(data, x, y, width) < threshold) << (word_len - 1 - x % word_len);
        }
    }
    stbi_image_free(data);

    potrace_param_t* param = potrace_param_default();
    potrace_state_t* state = potrace_trace(param, &bitmap);
    potrace_param_free(param);
    free(bitmap.map);
    if (state->status == POTRACE_STATUS_OK) {
        if (state->plist == NULL) return result;
        potrace_path_t* current_path =  state->plist;
        // each path is a separate line (packet) in rM terms
        while (current_path != NULL) {
            Point* points = NULL;
            potrace_curve_t current_curve = current_path->curve;
            // try to mimic real drawings
            // details (small area) are drawn with strokes that are smaller
            int line_width = 1 + floor(log10(current_path->area));
            for (int i = 0; i < current_curve.n; i++) {
                potrace_dpoint_t start = current_curve.c[i ? i-1 : current_curve.n-1][2];
                potrace_dpoint_t end = current_curve.c[i][2];
                // arrpush(points, new_point_with_width(translate_x, translate_y, start.x, start.y, line_width));
                if (current_curve.tag[i] == POTRACE_CORNER) {
                    arrpush(points, new_point_with_width(translate_x, translate_y, current_curve.c[i][1].x, current_curve.c[i][1].y, line_width));
                } else if (current_curve.tag[i] == POTRACE_CURVETO) { // bezier
                    potrace_dpoint_t u = current_curve.c[i][0];
                    potrace_dpoint_t w = current_curve.c[i][1];
                    int steps = infer_bezier_steps(start, u, w, end);
                    for (int j = 0; j < steps; j++) {
                        float t = j / (float)steps;
                        int bx = pow(1 - t, 3) * start.x + 3 * pow(1 - t, 2) * t * u.x +
                            3 * (1 - t) * pow(t, 2) * w.x + pow(t, 3) * end.x;
                        int by = pow(1 - t, 3) * start.y + 3 * pow(1 - t, 2) * t * u.y +
                            3 * (1 - t) * pow(t, 2) * w.y + pow(t, 3) * end.y;
                        arrpush(points, new_point_with_width(translate_x, translate_y, bx, by, line_width));
                    }
                }
                arrpush(points, new_point_with_width(translate_x, translate_y, end.x, end.y, line_width));
            }

            result += serialize_packet(create_packet(layer_id_major, layer_id_minor, (*id_counter)++, points), buf + result);
            arrfree(points);
            points = NULL;
            current_path = current_path->next;
        }
    }
    potrace_state_free(state);

    return result;
}

