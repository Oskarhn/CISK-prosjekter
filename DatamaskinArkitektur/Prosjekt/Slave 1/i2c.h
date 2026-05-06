/*
 * i2c.h - Felles I2C/TWI-bibliotek for smarthus-prosjekt
 * ING1507 Datamaskinarkitektur
 * ATmega32 @ 1MHz
 *
 * Statuskodereferanse (TWSR & 0xF8):
 * Master Transmitter (MT):
 *   0x08 = START sendt
 *   0x10 = Repeated START sendt
 *   0x18 = SLA+W sendt, ACK mottatt
 *   0x20 = SLA+W sendt, NACK mottatt
 *   0x28 = Data sendt, ACK mottatt
 *   0x30 = Data sendt, NACK mottatt
 * Master Receiver (MR):
 *   0x40 = SLA+R sendt, ACK mottatt
 *   0x48 = SLA+R sendt, NACK mottatt
 *   0x50 = Data mottatt, ACK sendt
 *   0x58 = Data mottatt, NACK sendt
 * Slave Receiver (SR):
 *   0x60 = SLA+W mottatt, ACK sendt
 *   0x80 = Data mottatt, ACK sendt
 *   0xA0 = STOP/Repeated START mottatt
 * Slave Transmitter (ST):
 *   0xA8 = SLA+R mottatt, ACK sendt
 *   0xB8 = Data sendt, ACK mottatt
 *   0xC0 = Data sendt, NACK mottatt
 */

#ifndef I2C_H
#define I2C_H

#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>

/* ---- Slave-adresser ---- */
#define SLAVE1_ADDR  0x10   /* Slave 1: inngang/stue   */
#define SLAVE2_ADDR  0x20   /* Slave 2: soverom        */

/* ---- Kommandoer master -> slave ---- */
#define CMD_DISARMED  0x00
#define CMD_ARMED     0x01
#define CMD_ALARM     0xAA

/* ---- Statusbytes slave -> master ---- */
#define STATUS_OK        0x00
#define STATUS_DOOR_OPEN 0x01

/*
 * TWI-frekvens:
 * TWBR = (F_CPU / (2 * F_SCL)) - 8  (prescaler = 1)
 * F_CPU = 1MHz, F_SCL = 50kHz
 * TWBR = (1000000 / (2 * 50000)) - 8 = 10 - 8 = 2
 */
#define TWI_BITRATE 2

/* Timeout-teller for I2C-operasjoner (hindrer evig blokkering) */
#define I2C_TIMEOUT 10000

/* ==========================================================
 *  MASTER-FUNKSJONER
 * ========================================================== */

void I2C_Master_Init(void)
{
    TWBR   = TWI_BITRATE;
    TWSR  &= ~((1 << TWPS1) | (1 << TWPS0)); /* Prescaler = 1 */
    PORTC |= (1 << PC0) | (1 << PC1);        /* Interne pull-ups SCL og SDA */
}

static void I2C_Start(void)
{
    TWCR = (1 << TWINT) | (1 << TWSTA) | (1 << TWEN);
    uint16_t t = I2C_TIMEOUT;
    while (!(TWCR & (1 << TWINT)) && --t);
}

static void I2C_Stop(void)
{
    TWCR = (1 << TWINT) | (1 << TWSTO) | (1 << TWEN);
    _delay_us(50);
}

static void I2C_Write(uint8_t data)
{
    TWDR = data;
    TWCR = (1 << TWINT) | (1 << TWEN);
    uint16_t t = I2C_TIMEOUT;
    while (!(TWCR & (1 << TWINT)) && --t);
}

static uint8_t I2C_Read_NACK(void)
{
    TWCR = (1 << TWINT) | (1 << TWEN); /* TWEA=0 -> sender NACK */
    uint16_t t = I2C_TIMEOUT;
    while (!(TWCR & (1 << TWINT)) && --t);
    return TWDR;
}

static uint8_t I2C_Status(void)
{
    return (TWSR & 0xF8);
}

/*
 * I2C_Master_Send - Sender en kommando-byte til en slave (MT-modus).
 * Returnerer 1 ved suksess, 0 ved feil.
 */
uint8_t I2C_Master_Send(uint8_t slave_addr, uint8_t cmd)
{
    I2C_Start();
    if (I2C_Status() != 0x08) { I2C_Stop(); return 0; }

    I2C_Write((slave_addr << 1) | 0);  /* SLA+W */
    if (I2C_Status() != 0x18) { I2C_Stop(); return 0; }

    I2C_Write(cmd);
    if (I2C_Status() != 0x28) { I2C_Stop(); return 0; }

    I2C_Stop();
    return 1;
}

/*
 * I2C_Master_Read - Les en byte direkte fra en slave (MR-modus).
 * Slave sender automatisk sin siste tx_data (slave_status eller current_temp).
 * Returnerer mottatt byte, eller 0xFF ved feil.
 */
uint8_t I2C_Master_Read(uint8_t slave_addr)
{
    I2C_Start();
    if (I2C_Status() != 0x08) { I2C_Stop(); return 0xFF; }

    I2C_Write((slave_addr << 1) | 1);  /* SLA+R */
    if (I2C_Status() != 0x40) { I2C_Stop(); return 0xFF; }

    uint8_t data = I2C_Read_NACK();    /* Eneste byte -> NACK -> STOP */
    I2C_Stop();
    return data;
}

/* ==========================================================
 *  SLAVE-FUNKSJONER (polling)
 * ========================================================== */

void I2C_Slave_Init(uint8_t own_addr)
{
    TWAR  = (own_addr << 1);                /* Sett slave-adresse  */
    TWCR  = (1 << TWEN) | (1 << TWEA);     /* Aktiver TWI + ACK   */
    PORTC |= (1 << PC0) | (1 << PC1);      /* Interne pull-ups    */
}

/*
 * I2C_Slave_Poll - Behandler en I2C-hendelse (ikke-blokkerende polling).
 *
 * rx_data : peker til buffer der mottatt kommando lagres
 * tx_data : byte som sendes tilbake til master ved lesing (ST-modus)
 *
 * Returnerer:
 *   1 = data mottatt fra master (SR) - rx_data er oppdatert
 *   2 = data sendt til master   (ST)
 *   0 = ingen fullstendig transaksjon ennaa
 */
uint8_t I2C_Slave_Poll(uint8_t *rx_data, uint8_t tx_data)
{
    if (!(TWCR & (1 << TWINT)))
        return 0;

    switch (I2C_Status())
    {
        case 0x60: /* SLA+W mottatt, ACK sendt */
            TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWEA);
            break;

        case 0x80: /* Data mottatt, ACK sendt */
            *rx_data = TWDR;
            TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWEA);
            return 1;

        case 0xA8: /* SLA+R mottatt - master vil lese */
            TWDR = tx_data;
            TWCR = (1 << TWINT) | (1 << TWEN); /* TWEA=0: siste byte */
            break;

        case 0xB8: /* Data sendt, ACK mottatt */
            TWCR = (1 << TWINT) | (1 << TWEN);
            break;

        case 0xC0: /* Data sendt, NACK mottatt - ferdig */
            TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWEA);
            return 2;

        case 0xA0: /* STOP eller Repeated START mottatt */
            TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWEA);
            break;

        default:
            /* Feil eller ukjent status - reset TWI */
            TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWEA);
            break;
    }
    return 0;
}

#endif /* I2C_H */
