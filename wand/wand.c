/*###############################################################################
;# TITLE   "WAND"	
;# 				
;#      Program         :41x Wand Code
;#      Version         :01.0
;#      Revision Date   :03/09/2008
;#      Author          :Alex Palmer
;#									

/*###############################################################################*/
#include <stdlib.h> 
#include <stdio.h>
#include <adc.h>
#include <delays.h>
#include <usart.h>
#pragma config OSC = HS
#pragma config DEBUG = ON

void init (void);
void main (void);
int data[5];

void main (void)
{
// Demo code to send a CAN message
//
//This will loop until the message has been moved into a free buffer. I don't think it will be too much of a problem.
init();

OpenUSART( USART_TX_INT_OFF  &
             USART_RX_INT_OFF  &
             USART_ASYNCH_MODE &
             USART_EIGHT_BIT   &
             USART_CONT_RX     &
		     BAUD_8_BIT_RATE  &
             USART_BRGH_HIGH,
             10 );
//10 = 115200
//129 = 9600
//baudUSART(BAUD_8_BIT_RATE & BAUD_WAKEUP_OFF & BAUD_AUTO_ON);

Delay10KTCYx(200);
Delay1KTCYx (255);



while(1)
{
LATC=0xFF;
Delay1KTCYx (255);

OpenADC( ADC_FOSC_32    &
         ADC_RIGHT_JUST &
         ADC_6_TAD,
         ADC_CH0        &
         ADC_INT_OFF & ADC_VREFPLUS_VDD & ADC_VREFMINUS_VSS, 15  );
//OpenADC( ADC_FOSC_32 & ADC_RIGHT_JUST , ADC_8ANA, ADC_CH0 & ADC_INT_OFF);
SetChanADC(ADC_CH0);
Delay10TCYx (255);
ConvertADC(); // Start conversion
while( BusyADC() ); // Wait for completion

CloseADC();
data[0] = ADRESH;
data[1] = ADRESL;

Delay10TCYx (255);
OpenADC( ADC_FOSC_32    &
         ADC_RIGHT_JUST &
         ADC_6_TAD,
         ADC_CH1        &
         ADC_INT_OFF & ADC_VREFPLUS_VDD & ADC_VREFMINUS_VSS, 15  );
//OpenADC( ADC_FOSC_32 & ADC_RIGHT_JUST, ADC_2ANA & ADC_INT_OFF & ADC_VREFPLUS_VDD & ADC_VREFMINUS_VSS, ADC_CH1);
SetChanADC(ADC_CH1);
Delay10TCYx (255);
ConvertADC(); // Start conversion
while( BusyADC() ); // Wait for completion

CloseADC();
data[2] = ADRESH;
data[3] = ADRESL;


data[0] = data[0] << 3;
data[0] = data[0] | ((data[1] & 0xE0) >> 5);
data[1] = data[1] & 0x1F;
data[1] = data[1] | 0xE0;
data[0] = data[0] | 0xE0;

data[2] = data[2] << 3;
data[2] = data[2] | ((data[3] & 0xE0) >> 5);
data[3] = data[3] & 0x1F;
data[3] = data[3] | 0xE0;
data[2] = data[2] | 0xE0;

data[5] = PORTC | 0xE0;

while(BusyUSART());
putcUSART(data[0]);
while(BusyUSART());
putcUSART(data[1]);
while(BusyUSART());
putcUSART(13);

while(BusyUSART());
putcUSART(data[2]);
while(BusyUSART());
putcUSART(data[3]);
while(BusyUSART());
putcUSART(13);

while(BusyUSART());
putcUSART(255);
while(BusyUSART());
putcUSART(data[5]);
while(BusyUSART());
putcUSART(13);
while(BusyUSART());
putcUSART(13);


}


CloseUSART();
while(1){
}

//Code it up


return ;
}


void init (void)
{
ADCON1=0x00;  // Set PORTA to all analog
TRISA=0xFF;
TRISB = 0b00001000;
PORTB = 0b00000000;

TRISC=0x01;


}
