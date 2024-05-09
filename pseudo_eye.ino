#include "Talkie.h"
#include "Vocab_US_Large.h"
int c;
Talkie voice;
int  a(int triggerPin,int repin)
{
  pinMode(triggerPin,OUTPUT);
  digitalWrite(triggerPin,LOW);  
   digitalWrite(triggerPin,HIGH);
  delay(10);
  digitalWrite(triggerPin,LOW);
   pinMode(repin,INPUT);
  return(pulseIn(repin,1));}
  
void setup ()
{
 Serial.begin(9600);
 pinMode(8,OUTPUT);
  pinMode(10,OUTPUT);
  digitalWrite(8,LOW);
  digitalWrite(10,LOW);
}

void loop(){
  
 float k=a(7,5);
  c=0.01723*k;
 if (c==0 || c<75) 
   {
   Serial.println("obj dist is");
   Serial.println(c);
  
   Serial.println("move left");
   voice.say(sp2_LEFT);
   digitalWrite(8,HIGH);
   
  delay(1000);
   digitalWrite(8,LOW);
   int l=a(7,5);
   int c1=0.01723*l;
   
  if (c1==0 || c1<75) 
  {
   Serial.println("obj dist is");
   Serial.println(c1);
   Serial.println("move right");
   voice.say(sp2_RIGHT);
 digitalWrite(10,HIGH);
 delay(1000);
 digitalWrite(10,LOW);
    int m,c2;
    m=a(7,5);
     c2=0.01723*m;
    if (c2==0 || c2<75) 
  {
   Serial.println("obj dist is");
   Serial.println(c2);
   
   delay(1000);
     }
    
  }
   
 }
 else
 {
    Serial.println("obj not");
     voice.say(sp2_GO);
     delay(1000);
   
 }}
