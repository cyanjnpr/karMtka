#pragma once

#include <stddef.h>

#ifndef INCLUDE_LIBSKETCH_H
#define INCLUDE_LIBSKETCH_H

typedef char leb128;

typedef struct __attribute__((__packed__)) {
    int length;
    char first_ver;
    char min_ver;
    char ver;
    char type;
} PacketHeader;

typedef struct __attribute__((__packed__)) {
    float x;
    float y;
    short speed;
    short width;
    char direction;
    char pressure;
} Point;

typedef struct __attribute__((__packed__)) {
    char length_sig;
    int length;
    char unknown_byte; // 3

    char tool_sig;
    int tool;
    char color_sig;
    int color;
    char thickness_scale_sig;
    double thickness_scale;
    char starting_length_sig;
    int starting_length;

    char points_length_sig;
    int points_length;
    Point* points;
    char ts_sig;
    leb128* ts;
} LinePoints;

typedef struct __attribute__((__packed__)) {
    PacketHeader header;

    char parent_id_sig;
    leb128* parent_id;
    char id_sig;
    leb128* id;
    char left_sig;
    leb128* left;
    char right_sig;
    leb128* right;
    char deleted_length_sig;
    int deleted_length;

    LinePoints line;
} LinePacket;

PacketHeader create_header();

LinePoints create_line(Point* points);

void encode_leb128(int val, leb128** buf);

void encode_id(int major, int minor, char** buf);

int pixel_to_value(int val, int alpha);

int value_to_shade(int val, int shades);

size_t image_to_points(char* filename, int layer_id, int counter, int shades, char* buf);

int get_pixel(stbi_uc* data, int x, int y);

size_t serialize_packet(LinePacket packet, char* dest);

#endif
