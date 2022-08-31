import React, { Component, useEffect, useState } from 'react';
import Webcam from "react-webcam";
import Canvas from '../components/Canvas'
const WebcamComponent = () => <Webcam />;


const IMG_FACTOR = 60;
const NUM_IMAGES_INIT = 5


const WebcamCapture = ({saveInitImage, 
                        saveARImage, 
                        saveNavImage, 
                        sendInitRequest,  
                        isGoal, 
                        width, 
                        height, 
                        markerDirUpDown, 
                        markerPosUpDown, 
                        markerDirLeftRight, 
                        markerPosLeftRight}) => {

    const webcamRef = React.useRef(null);
    const [showCaptureInfo, setShowCaptureInfo] = React.useState(false)
    const videoConstraints = {
        width: width,
        
        facingMode: "user",
        aspectRatio: 9/16
    };

    const [counter, setCounter] = React.useState(0)

    const capture = (usageReason) => {
        const imageSrc = webcamRef.current.getScreenshot();

        if (usageReason === "AR"){
            saveARImage(imageSrc)
        } else if(usageReason === "Nav"){
            saveNavImage(imageSrc)
        } else {
            saveInitImage(imageSrc);
        }
    }

    //Captures 5 photos for the initial navigation
    const capturePhotosForStart = (e) => {
        e.preventDefault();
        let numImages = 0
        setShowCaptureInfo(true)

        const timerId = setInterval(() => {
            capture("Init")
            numImages++;
            if(numImages >= NUM_IMAGES_INIT) {
                clearInterval(timerId);
                setShowCaptureInfo(false)
                sendInitRequest()
                numImages = NUM_IMAGES_INIT
                captureImagePriodicallyForNavigation()
                captureImagePriodicallyForAR()
            }
        }, 750)
    }

    //captures every 1000 ms a new image for the ar request
    const captureImagePriodicallyForAR = () => {
        const timerId = setInterval(() => { 
            capture("AR")
            clearInterval(timerId)
            if(isGoal){
                clearInterval(timerId)
            }
        }, 1000)
    }

    //captures every 1000 ms a new image for the navigation request
    const captureImagePriodicallyForNavigation = () => {
        const timerId = setInterval(() => { 
            capture("Nav")
            setCounter(counter++)
            if(isGoal){
                clearInterval(timerId)
            }
        }, 1000)
    }
    return (
        <div className="webcam-container"  >
            <div style={{position: 'relative', width: width, height:height}}>
                {width && height && <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpg"
                    videoConstraints={videoConstraints}
                    forceScreenshotSourceSize="true"
                    style={{position: 'absolute', top: '0', left: '0', height: height, width:'100%', objectFit:"cover"}}
                />}
                {width && height && <Canvas 
                    width={width} 
                    height={height} 
                    markerPosUpDown={markerPosUpDown}
                    markerDirUpDown={markerDirUpDown}
                    markerPosLeftRight={markerPosLeftRight}
                    markerDirLeftRight={markerDirLeftRight}
                    style={{position: 'absolute', top: '0', left: '0'}}
                />}
            </div>
            
            {showCaptureInfo && 
                <div>Schwenke die Kamera für genauere Bestimmung des Startpunktes </div>}
            <button 
                onClick={(e) => {capturePhotosForStart(e)}}>
                Starte Navigation
            </button>
        </div>
    );
}

export default WebcamCapture;
