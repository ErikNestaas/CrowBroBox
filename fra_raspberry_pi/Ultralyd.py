from gpiozero import DistanceSensor
# from time import sleep

def get_us_distance(echo, trigger): # Input er GPIO-pinnene som brukes for echo og trigger (varierer for de forksjellige sensorene)
    ultrasonic = DistanceSensor(echo=echo, trigger=trigger)
    try:
        distance_m = ultrasonic.distance
        print(f"Avstand meter: {distance_m}") # Debug
        return distance_m
        
    except KeyboardInterrupt:
        print("Measurement stopped by user") # Hvis bruker trykker Ctrl+C
    
    except SystemError:
        print("Noe gikk galt?")
    
#get_us_distance(4, 17)
    # GIT Notater: add (for hvilke filer du vil stage), commit (for å committe endringene (lokalt)), push (for å pushe endringene (på Hub)), 
    
