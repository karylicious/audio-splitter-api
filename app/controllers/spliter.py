from flask_restful import Resource
from flask import Flask, send_file, request , jsonify
import shutil
from support.file import FileHandler
import subprocess
import os
from utils import ROOT_DIR

class Splitter(Resource):
    def post(self):
        if( 'audiofile' not in request.files):
            return jsonify({"Error": 'Expected audiofile argument'})
    
        intendedFile = request.files['audiofile']

        if(intendedFile.filename == ''):
            return jsonify({"Error": 'No file has been sent'})

        if (not intendedFile.filename.lower().endswith('.mp3')):
            return jsonify({"Error": 'Invalid file. Expected .mp3 format'})
            
        
        fileHandler = FileHandler()        
        userDirectoryName = fileHandler.createUserDirectory()
        fileHandler.uploadFile(userDirectoryName, intendedFile)
        return jsonify({"userdirectoryname": userDirectoryName})

    def get(self):      
        if( 'userdirectoryname' not in request.args):
            return jsonify({"Error": 'Expected userdirectoryname argument'})
            
        if( 'filename' not in request.args):
            return jsonify({"Error": 'Expected filename argument'})
    
        args = request.args

        if(args['userdirectoryname'] == ''):
            return jsonify({"Error": 'userdirectoryname is invalid'})
            
        if(args['filename'] == ''):
            return jsonify({"Error": 'filename is invalid'})
            
        userDirectoryName = args['userdirectoryname']
        filename = args['filename']
        uploadedFilePath = ROOT_DIR +'/temp/'+ userDirectoryName + '/' + filename

        spleeter_cmd = ['python3', '-m', 'spleeter','separate', '-i',
        uploadedFilePath, '-p', 'spleeter:2stems-16kHz',
        '-o', 'temp/' + userDirectoryName]
        subprocess.run(spleeter_cmd, cwd='spleeter')
        
        fileHandler = FileHandler() 
        fileHandler.zipDirectory(userDirectoryName)
        createdZipFile = ROOT_DIR +'/temp/'+ userDirectoryName + '/' + userDirectoryName + '.zip'
        fileName = userDirectoryName + '.zip'

        return send_file(createdZipFile, mimetype='application/x-zip-compressed', as_attachment=True, attachment_filename=fileName)

    def delete(self):
        if( 'userdirectoryname' not in request.args):
                return jsonify({"Error": 'Expected userdirectoryname argument'})

        userdirectoryname = request.args['userdirectoryname']

        if(userdirectoryname == ''):
            return jsonify({"Error": 'userdirectoryname is invalid'})

        fileHandler = FileHandler() 
        fromTempDirectory = 'temp'
        fileHandler.deleteDirectory(fromTempDirectory, userdirectoryname)

        fromSpleeterTempDirectory = 'spleeter/temp'
        fileHandler.deleteDirectory(fromSpleeterTempDirectory, userdirectoryname)
       
        return jsonify({"Succeed": True})