from gpiozero import DistanceSensor
# from time import sleep

def get_us_distance(echo, trigger): # Input er GPIO-pinnene som brukes for echo og trigger (varierer for de forksjellige sensorene)
    ultrasonic = DistanceSensor(echo=echo, trigger=trigger)
    try:
        distance_m = ultrasonic.distance
        return distance_m
        # print(f"Avstand meter: {distance_m:.3f:}") # Debug
    except KeyboardInterrupt:
        print("Measurement stopped by user") # Hvis bruker trykker Ctrl+C
    
    except SystemError:
        print("Noe gikk galt?")
    

    # GIT Notater: add (for hvilke filer du vil stage), commit (for å committe endringene (lokalt)), push (for å pushe endringene (på Hub)), 
    