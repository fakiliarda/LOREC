#!/usr/bin/env python3
import argparse
import os
import mysql.connector
from picamera import PiCamera
from time import time, strftime
from time import sleep
import datetime
import threading

from aiy.leds import Leds
from aiy.leds import PrivacyLed
from aiy.toneplayer import TonePlayer
from aiy.vision.annotator import Annotator

from aiy.vision.inference import CameraInference
from aiy.vision.models.LorecModels import ObjectDetection
from aiy.vision.models.LorecModels import FaceDetection

# Sound setup
MODEL_LOAD_SOUND = ('C6w', 'c6w', 'C6w')
BEEP_SOUND = ('E6q', 'C6q')
player = TonePlayer(gpio=22, bpm=30)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num_frames',
        '-f',
        type=int,
        dest='num_frames',
        default=-1,
        help='Sets the number of frames to run for, otherwise runs forever.')

    parser.add_argument(
        '--num_pics',
        '-p',
        type=int,
        dest='num_pics',
        default=-1,
        help='Sets the max number of pictures to take, otherwise runs forever.')

    cnx = mysql.connector.connect(user='root', password='aey.1996',
                             host='34.65.17.107',
                            database='lorecdb')
    cursor = cnx.cursor()


    args = parser.parse_args()
    

    with PiCamera() as camera, PrivacyLed(Leds()):
        # See the Raspicam documentation for mode and framerate limits:
        # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
        # Set to the highest resolution possible at 16:9 aspect ratio
        camera.sensor_mode = 4
        camera.resolution = (1640, 1232)
        #camera.start_preview(fullscreen=True)


        def facedet():
            with CameraInference(FaceDetection.model()) as inference:
                for result in inference.run(args.num_frames):
                    faces = FaceDetection.get_faces(result)
                    annotator.clear()
                    for face in faces:
                        annotator.bounding_box(transform(face.bounding_box), fill=0)
                    annotator.update()

                    print('#%05d (%5.2f fps): num_faces=%d, avg_joy_score=%.2f' %
                    (inference.count, inference.rate, len(faces), avg_joy_score(faces)))
                
        def objdet():
            with CameraInference(ObjectDetection.model()) as inference:
                print("Camera inference started")
                player.play(*MODEL_LOAD_SOUND)
            
                last_time = time()
                pics = 0
                save_pic = False

                #enable_label = True
                # Annotator renders in software so use a smaller size and scale results
                # for increased performace.
                #annotator = Annotator(camera, dimensions=(320, 240))
                scale_x = 320 / 1640
                scale_y = 240 / 1232
                # Incoming boxes are of the form (x, y, width, height). Scale and
                # transform to the form (x1, y1, x2, y2).
                def transform(bounding_box):
                    x, y, width, height = bounding_box
                    return (scale_x * x, scale_y * y, scale_x * (x + width),
                        scale_y * (y + height))
					
                def leftCorner(bounding_box):
                    x, y, width, height = bounding_box
                    return (scale_x * x, scale_y * y)
				
                def truncateFloat(value):
                    return '%.3f'%(value)

                for f, result in enumerate(inference.run()):
			
                    #annotator.clear()
                    detections = enumerate(ObjectDetection.get_objects(result, 0.3))

                    for i, obj in detections:
                        print('%s',obj.label)
                        #annotator.bounding_box(transform(obj.bounding_box), fill=0)
                        #if enable_label:
                            #annotator.text(leftCorner(obj.bounding_box),obj.label + " - " + str(truncateFloat(obj.score)))
             
                        print('%s Object #%d: %s' % (strftime("%Y-%m-%d-%H:%M:%S"), i, str(obj)))
                        x, y, width, height = obj.bounding_box
                        dt = datetime.datetime.now()
                        if obj.label == 'person':
                            os.system("ffplay -nodisp -autoexit  LorecObjectSoundFiles/Kisialgilaniyor.mp3")
                            query = ("INSERT INTO Log (Tag, Time, LocLatitude, LocLongitude, GlassNameDbid, ModuleDbid) VALUES ('İnsan', '"+str(dt) +"', '39.888346', '32.655403', '1', '2')")
                            cursor.execute(query)
                            for something in cursor:
                                print(something)
                            cnx.commit()
                            #save_pic = True
                            #player.play(*BEEP_SOUND)
                        elif obj.label == 'tvmonitor':
                            os.system("ffplay -nodisp -autoexit  LorecObjectSoundFiles/Ekran.mp3")
                            query = ("INSERT INTO Log (Tag, Time, LocLatitude, LocLongitude, GlassNameDbid, ModuleDbid) VALUES ('Ekran', '"+str(dt) +"', '39.888346', '32.655403', '1', '2')")
                            cursor.execute(query)
                            for something in cursor:
                                print(something)
                            cnx.commit()
                        elif obj.label == 'car':
                            os.system("ffplay -nodisp -autoexit  LorecObjectSoundFiles/Otomobil.mp3")
                            query = ("INSERT INTO Log (Tag, Time, LocLatitude, LocLongitude, GlassNameDbid, ModuleDbid) VALUES ('Otomobil', '"+str(dt) +"', '39.888346', '32.655403', '1', '2')")
                            cursor.execute(query)
                            for something in cursor:
                                print(something)
                            cnx.commit()
                        elif obj.label == 'chair':
                            os.system("ffplay -nodisp -autoexit  LorecObjectSoundFiles/Sandalye.mp3")
                            query = ("INSERT INTO Log (Tag, Time, LocLatitude, LocLongitude, GlassNameDbid, ModuleDbid) VALUES ('Sandalye', '"+str(dt) +"', '39.888346', '32.655403', '1', '2')")
                            cursor.execute(query)
                            for something in cursor:
                                print(something)
                            cnx.commit()
                    # save the image
                    if save_pic:
                        # save the clean image
                        camera.capture("images/image_%s.jpg" % strftime("%Y%m%d-%H%M%S"))
                        pics += 1
                        save_pic = False

                    if f == args.num_frames or pics == args.num_pics:
                        breakc

                    #annotator.update()
                    now = time()
                    duration = (now - last_time)

                    # The Movidius chip runs at 35 ms per image.
                    # Then there is some additional overhead for the object detector to
                    # interpret the result and to save the image. If total process time is
                    # running slower than 50 ms it could be a sign the CPU is geting overrun
                    if duration > 0.50:
                        print("Total process time: %s seconds. Bonnet inference time: %s ms " %
                              (duration, result.duration_ms))

                    last_time = now


        
        #threading.Thread(target=facedet).start()
        objdet()
        #sleep(200)
        #camera.stop_preview()


if __name__ == '__main__':
    main()
