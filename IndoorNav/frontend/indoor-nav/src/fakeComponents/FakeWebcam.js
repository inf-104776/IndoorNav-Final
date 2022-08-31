import fakeImg from './fakeImg.jpg'
import React, { Component, useEffect, useState } from 'react';
import Canvas from '../components/Canvas'

const NUM_IMAGES_INIT = 5

const FakeWebcam = ({
    test,
    saveInitImage, 
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

    const [showCaptureInfo, setShowCaptureInfo] = React.useState(false)

    const capture = (usageReason) => {
        const imageSrc = fakeImg //TODO load

        if (usageReason === "AR"){
            console.log("AR")
            saveARImage(imageSrc)
        } else if(usageReason === "Nav"){
            saveNavImage(imageSrc)
        } else {
            saveInitImage(imageSrc);
        }
    }

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

    const captureImagePriodicallyForAR = () => {
        const timerId = setInterval(() => { 
            capture("AR")
            clearInterval(timerId)
            if(isGoal){
                clearInterval(timerId)
            }
        }, 3000)
    }
    
    const captureImagePriodicallyForNavigation = () => {
        const timerId = setInterval(() => { 


            capture("Nav")

            if(isGoal){
                clearInterval(timerId)
            }
            
        }, 3000)
    }

    let fakeWebcam = <div><img
        src={fakeImg}
        alt="fake image"
        />
        </div>

    return (
        <div className="webcam-container"  >
            <div style={{position: 'relative', width: width, height:height, margin: '0 auto'}}>
                
                {width && height && fakeWebcam}
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
            <div> <div>Schwenke die Kamera für  </div>
                <div>genauere Bestimmung des Startpunktes </div></div>
                }
            <button 
                onClick={(e) => {capturePhotosForStart(e)}}>
                Starte Navigation
            </button>
        </div>
    );
}

export default FakeWebcam;