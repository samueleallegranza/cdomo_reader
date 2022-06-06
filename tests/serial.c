#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdint.h>

#include <wiringPi.h>
#include <wiringSerial.h>

#define SERIAL_INTERFACE "/dev/ttyUSB0"
#define SERIAL_BAUDRATE 115200

typedef union cmd_reqvals_s{
    uint8_t packet;
    struct _packet_s{
        uint8_t addr    : 1;
        uint8_t cmd     : 4;
        uint8_t counter : 1;
        uint8_t crc_lsb : 1;
        uint8_t crc_msb : 1;
    };
} cmd_reqvals_t;

typedef struct example_s
{
    uint8_t addr : 4;
} example_t;

int main(int argc, char * argv[]) {
    int fd;
    example_t msg_test;

    if ((fd = serialOpen(SERIAL_INTERFACE, 115200)) < 0)
    {
        fprintf(stderr, "Unable to open serial device: %s\n", strerror(errno));
        return 1;
    }

    if (wiringPiSetup() == -1)
    {
        fprintf(stdout, "Unable to start wiringPi: %s\n", strerror(errno));
        return 1;
    }

    msg_test.addr = 0x12;
    printf("%x", msg_test.addr);

    serialClose(fd);

    return 0;
}
