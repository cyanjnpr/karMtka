#pragma once

#include <stddef.h>

#ifndef INCLUDE_LIBSKETCH_H
#define INCLUDE_LIBSKETCH_H

typedef char leb128;

enum PacketTypes {
    LINE_PACKET = 0x05
};

enum SketchTools {
    TOOL_PAINTBRUSH = 12,
    TOOL_MECHANICAL = 13,
    TOOL_PENCIL = 14,
    TOOL_BALLPOINT = 15,
    TOOL_MARKER = 16,
    TOOL_FINELINER = 17,
    TOOL_HIGHLIGHTER = 18,
    TOOL_CALIGRAPHY = 21
};

enum SketchColors {
    COLOR_BLACK = 0,
    COLOR_GRAY = 1,
    COLOR_WHITE = 2
};

typedef struct __attribute__((__packed__)) {
    unsigned int length;
    unsigned char first_ver;
    unsigned char min_ver;
    unsigned char ver;
    unsigned char type;
} PacketHeader;

typedef struct __attribute__((__packed__)) {
    float x;
    float y;
    unsigned short speed;
    unsigned short width;
    unsigned char direction;
    unsigned char pressure;
} Point;

typedef struct {
    unsigned char length_sig;
    unsigned int length;
    unsigned char unknown_byte; // 3

    unsigned char tool_sig;
    unsigned int tool;
    unsigned char color_sig;
    unsigned int color;
    unsigned char thickness_scale_sig;
    double thickness_scale;
    unsigned char starting_length_sig;
    unsigned int starting_length;

    unsigned char points_length_sig;
    unsigned int points_length;
    Point* points;
    unsigned char ts_sig;
    leb128* ts;
} LinePoints;

typedef struct {
    PacketHeader header;

    unsigned char parent_id_sig;
    leb128* parent_id;
    unsigned char id_sig;
    leb128* id;
    unsigned char left_sig;
    leb128* left;
    unsigned char right_sig;
    leb128* right;
    unsigned char deleted_length_sig;
    unsigned int deleted_length;

    LinePoints line;
} LinePacket;

unsigned char sig_len(unsigned char val);
unsigned char sig_id(unsigned char val);
unsigned char sig_int(unsigned char val);
unsigned char sig_dbl(unsigned char val);

PacketHeader create_header();

LinePoints create_line(Point* points);

LinePacket create_packet(int layer_id, int counter, Point* points);

void encode_leb128(int val, leb128** buf);

void encode_id(int major, int minor, char** buf);

int pixel_to_value(int val, int alpha);

int value_to_shade(int val, int shades);

int get_pixel(stbi_uc* data, int x, int y, int width);

size_t serialize_packet(LinePacket packet, char* dest);

size_t convert(char* filename, int page_width, int page_height, int margin, int layer_id, int* id_counter, int shades, char* buf);

#endif
