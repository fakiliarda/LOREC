# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import os
import re
import face_recognition.api as face_recognition
import multiprocessing
import itertools
import sys
import PIL.Image
import numpy as np
import time
import mysql.connector

def start():
    known_names, known_face_encodings = scan_known_people("known_people")
    while 1:
        connection = mysql.connector.connect(user='root', password='aey.1996',
                              host='34.65.17.107',
                              database='lorecdb')
        cursor = connection.cursor()
        sql_query = """SELECT * from faces where isRecieved=0"""
        cursor.execute(sql_query)
        result=cursor.fetchall()
        if not result:
            print("No recieved images...Waiting...")
            #time.sleep(0.2)
        else:
            id=result[0][0]
            photo=result[0][1]
            result=""
            save_file(photo, "unknown.jpg")
            recognize("unknown.jpg", 1, 0.6, False, known_names, known_face_encodings, id)
            print("Recognized")
            sql_query = ('update faces set isRecieved=1 where id='+str(id)+'')
            cursor.execute(sql_query)
            connection.commit()
			
            print("Inserted to DB")
            connection.close()
def save_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

        if len(encodings) == 0:
            click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings


def send_result(filename, name, distance, id, show_distance=False):
    print(name)
    connection = mysql.connector.connect(user='root', password='aey.1996',
                        host='34.65.17.107',
                        database='lorecdb')
    cursor = connection.cursor()
    sql_query = ('INSERT INTO facetags (id, tag) values ('+str(id)+',"'+name+'");')
    cursor.execute(sql_query)
    connection.commit()
    connection.close()


def test_image(image_to_check, known_names, known_face_encodings, id, tolerance=0.6, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        if True in result:
            [send_result(image_to_check, name, distance, id, show_distance) for is_match, name, distance in zip(result, known_names, distances) if is_match]
        else:
            send_result(image_to_check, "unknown_person", None, id, show_distance)

    if not unknown_encodings:
        # print out fact that no faces were found in image
        send_result(image_to_check, "no_persons", None, id, show_distance)


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

    # macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods():
        context = multiprocessing.get_context("forkserver")

    pool = context.Pool(processes=processes)

    function_parameters = zip(
        images_to_check,
        itertools.repeat(known_names),
        itertools.repeat(known_face_encodings),
        itertools.repeat(tolerance),
        itertools.repeat(show_distance)
    )

    pool.starmap(test_image, function_parameters)

def recognize(image_to_check, cpus, tolerance, show_distance, known_names, known_face_encodings, id):

    # Multi-core processing only supported on Python 3.4 or greater
    if (sys.version_info < (3, 4)) and cpus != 1:
        click.echo("WARNING: Multi-processing support requires Python 3.4 or greater. Falling back to single-threaded processing!")
        cpus = 1

    if os.path.isdir(image_to_check):
        if cpus == 1:
            [test_image(image_file, known_names, known_face_encodings, id, tolerance, show_distance) for image_file in image_files_in_folder(image_to_check)]
        else:
            process_images_in_process_pool(image_files_in_folder(image_to_check), known_names, known_face_encodings, cpus, tolerance, show_distance)
    else:
        test_image(image_to_check, known_names, known_face_encodings, id, tolerance, show_distance)


if __name__ == "__main__":
    start()
