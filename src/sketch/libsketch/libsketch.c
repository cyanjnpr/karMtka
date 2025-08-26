#include <stdbool.h>

#define STB_DS_IMPLEMENTATION
#include "stb_ds.h"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_resize2.h"

#include "libsketch.h"

// xochitl won't render a line consisting of more points
const int MAX_POINTS = 30000;
const int POINTS_CAP = 0.7 * MAX_POINTS;

const int TOOL_MECHANICAL = 13;
const int COLOR_BLACK = 0;

Point new_point(float x, float y, int val, int shades) {
    return (Point){x, y, 1, 
        0 ? value_to_shade(val, shades) == shades : 1, 
        0, (char)(0xff - val)};
}

PacketHeader create_header() {
    return (PacketHeader){0, 0x00, 0x02, 0x02, 0x05};
}

LinePoints create_line(Point* points) {
    LinePoints line = {
        .length_sig = 0x6C, .length = 0,
        .unknown_byte = 0x03,
        .tool_sig = 0x14, .tool = TOOL_MECHANICAL,
        .color_sig = 0x24, .color = COLOR_BLACK,
        .thickness_scale_sig = 0x38, .thickness_scale = 1.0,
        .starting_length_sig = 0x44, .starting_length = 0,
        .points_length_sig = 0x5C, .points_length = 14 * arrlen(points),
        .points = points,
        .ts_sig = 0x6F, .ts = NULL
    };
    encode_id(0, 1, &line.ts);
    line.length = 31 + arrlen(line.points) * 14 + arrlen(line.ts);
    return line;
}

LinePacket create_packet(int layer_id, int counter, Point* points) {
    LinePacket packet = {
        .header = create_header(),
        .parent_id_sig = 0x1F, .parent_id = NULL,
        .id_sig = 0x2F, .id = NULL,
        .left_sig = 0x3F, .left = NULL,
        .right_sig = 0x4F, .right = NULL,
        .deleted_length_sig = 0x54, .deleted_length = 0,
        .line = create_line(points)
    };
    encode_id(1, layer_id, &packet.parent_id);
    encode_id(1, counter, &packet.id);
    encode_id(0, 0, &packet.left);
    encode_id(0, 0, &packet.right);
    packet.header.length = 9 + 5 + packet.line.length + arrlen(packet.parent_id) + arrlen(packet.id) + arrlen(packet.left) + arrlen(packet.right);
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
    return value_to_shade(get_pixel(data, following_x, y), shades);
}

int get_pixel(stbi_uc* data, int x, int y) {
    int i = (y*x + x) * 2;
    return pixel_to_value(data[i], data[i+1]);
}

size_t serialize_packet(LinePacket packet, char* dest) {
    long n = 0;
    memcpy(dest + n, &packet, 9); n += 9;
    memcpy(dest + n, packet.parent_id, arrlen(packet.parent_id)); n += arrlen(packet.parent_id);
    memcpy(dest + n, &packet.id_sig, 1); n += 1;
    memcpy(dest + n, packet.id, arrlen(packet.id)); n += arrlen(packet.id);
    memcpy(dest + n, &packet.left_sig, 1); n += 1;
    memcpy(dest + n, packet.left, arrlen(packet.left)); n += arrlen(packet.left);
    memcpy(dest + n, &packet.right_sig, 1); n += 1;
    memcpy(dest + n, packet.right, arrlen(packet.right)); n += arrlen(packet.right);
    memcpy(dest + n, &packet.deleted_length_sig, 1); n += 1;
    memcpy(dest + n, &packet.deleted_length, 4); n += 4;
    memcpy(dest + n, &packet.line, 35); n += 35;
    memcpy(dest + n, packet.line.points, arrlen(packet.line.points) * 14); n += arrlen(packet.line.points) * 14;
    memcpy(dest + n, &packet.line.ts_sig, 1); n += 1;
    memcpy(dest + n, packet.line.ts, arrlen(packet.line.ts)); n += arrlen(packet.line.ts);
    return n;
}

size_t image_to_points(char* filename, int layer_id, int counter, int shades, char* buf) {
    int width = 0;
    int height = 0;
    int channels = 0;
    stbi_uc* data = stbi_load(filename, &width, &height, &channels, 2);
    if (data == NULL) {
        return 0;
    }

    Point* points = NULL;
    int previous_shade = -1;
    bool left_to_right = true;
    for (int y = 0; y < height; y++) {
        if (left_to_right) {
            for (int x = 0; x < width; x++) {
                int val = get_pixel(data, x, y);
                int shade = value_to_shade(val, shades);
                if (previous_shade != shade || following_pixel_shade(
                        data, x+1, y, shades, width) != shade) {
                    previous_shade = shade;
                    arrpush(points, new_point((float)x, (float)y, val, shades));
                }
            }
        } else {
            for (int x = width - 1; x >= 0; x--) {
                int val = get_pixel(data, x, y);
                int shade = value_to_shade(val, shades);
                if (previous_shade != shade || following_pixel_shade(
                        data, x-1, y, shades, width) != shade) {
                    previous_shade = shade;
                    arrpush(points, new_point((float)x, (float)y, val, shades));
                }
            }
        }
        left_to_right = !left_to_right;
    }
    stbi_image_free(data);

    LinePacket packet = create_packet(layer_id, counter, points);
    return serialize_packet(packet, buf);

    // printf("Points: %ld\n", arrlen(points));
    // memcpy(buf, points, arrlen(points) * 14);
    // return arrlen(points) * 14;
}

