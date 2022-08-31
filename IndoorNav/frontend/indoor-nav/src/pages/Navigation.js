import WebcamCapture from "../components/WebcamCapture"
import React, { Component, useEffect, useState } from 'react';
import Select from 'react-select'
import NavInfo from '../components/NavInfo'
import Canvas from '../components/Canvas'
import FakeWebcam from "../components/FakeWebcam";

let urlInitialNavigation = "http://127.0.0.1:5000/initial_navigation"
let urlAR = "http://127.0.0.1:5000/ar"
let urlNavigation = "http://127.0.0.1:5000/navigation"

const IMG_FACTOR = 20;
const WIDTH = 9 * IMG_FACTOR
const HEIGHT = 16 * IMG_FACTOR

function dataURLtoFile(dataurl, filename) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
}

function Navigation() {
    const [images, setImages] = React.useState([])
    const [dest, setDest] = React.useState('')
    const [isGoal, setIsGoal] = React.useState(false)

    const [nextDir, setNextDir] = React.useState('')
    const [currDir, setCurrDir] = React.useState('')
    const [dist, setDist] = React.useState(0)
    const [navImage, setNavImage] = React.useState()
    const [navResponsePresent, setNavResponsePresent] = React.useState(false)

    const [markerDirUpDown, setMarkerDirUpDown] = React.useState()
    const [markerPosUpDown, setMarkerPosUpdown] = React.useState([])
    const [markerDirLeftRight, setMarkerDirLeftRight] = React.useState()
    const [markerPosLeftRight, setMarkerPosLeftRight] = React.useState()
    const [arImage, setARImage] = React.useState()
    const [arResponsePresent, setARResponsePresent] = React.useState(true)

    const [initComplete, setInitComplete] = React.useState(false)

    //TODO add other options
    const options = [
        { value: "A2.06", label: "Seminarraum 6" },
        { value: "A2.06", label: "SR6" },
        { value: "A2.06", label: "Aristoteles" },
    ]

    const saveInitImage = (image) => {
        var file = dataURLtoFile(image, images.length + '.jpg'); //dont need that when using fakeWebcam 
        let new_images = images
        new_images.push(file)
        new_images.push(image)
        setImages(new_images)
    }

    const saveNavImage = (image) => {
        var file = dataURLtoFile(image, 'navImage.jpg');
        setNavImage(file)
        //setNavImage(image) //only when using fakeWebcam
    }

    const saveARImage = (image) => {
        var file = dataURLtoFile(image, 'ARImage.jpg');
        setARImage(file)
        //setARImage(image) //only when using fakeWebcam
    }

    //send initial navigation request
    const sendInitialNavigationRequest = () => {

        const formData = new FormData();
        //send images via form data
        for (let i = 0; i < images.length; i++) {
            formData.append('images', images[i]);
        }

        formData.append('destination', dest)

        setImages([])
        fetch(urlInitialNavigation, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.is_goal !== undefined) {
                    setIsGoal(true)
                } else {
                    setDist(data.dist_next_turn)
                    setCurrDir(data.pos_dir.slice(-1))
                    setNextDir(data.dir_next_turn)
                    
                    setInitComplete(true)
                }
            });
    }

    //send normal navigation request
    useEffect(() => {
        if(initComplete && navImage){
            const formData = new FormData();

            formData.append('images', navImage);
            setNavResponsePresent(false)
            
            setNavImage()
            fetch(urlNavigation, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_goal !== undefined) {
                    setIsGoal(true)
                } else {
                    setDist(data.dist_next_turn)
                    setCurrDir(data.pos_dir.slice(-1))
                    setNextDir(data.dir_next_turn)
                    setNavImage(navImage)
                }
            });
        }
        
    }, [navImage, initComplete])
    

    //send AR Request
    useEffect(() => {
        if(initComplete && arImage ){
            setARResponsePresent(false)
            const formData = new FormData();
            formData.append('images', arImage);
            fetch(urlAR, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                setARResponsePresent(true)
                if (data.dest_reached) {
                    setIsGoal(true)
                } else {
                    setMarkerDirLeftRight(data.left_right_dir)
                    setMarkerPosLeftRight(data.left_right_pos)
                    setMarkerDirUpDown(data.up_down_dir)
                    setMarkerPosUpdown(data.up_down_pos)  
                }
            });
        }
        
    },[arImage, initComplete, navImage])
    
    const onChangeSelect = (selection) => {
        
        setDest(selection.value)
        send_init_request()
    }

    const webcam = <WebcamCapture
            saveInitImage={saveInitImage}
            saveARImage={saveARImage}
            saveNavImage={saveNavImage}
            sendInitRequest={sendInitialNavigationRequest}
            isGoal={isGoal}
            width={WIDTH}
            height={HEIGHT}
            style={{position: 'absolute',top: '0', left: '0', width: WIDTH, height: HEIGHT}}
/>

    //switch to fakecam to mock video
    const fakecam = <FakeWebcam
        test={"abc"}
        saveInitImage={saveInitImage}
        saveARImage={saveARImage}
        saveNavImage={saveNavImage}
        sendInitRequest={sendInitialNavigationRequest}
        isGoal={isGoal}
        width={WIDTH}
        height={HEIGHT}
        markerDirUpDown={markerDirUpDown}
        markerDirLeftRight={markerDirLeftRight}
        markerPosUpDown={markerPosUpDown}
        markerPosLeftRight={markerPosLeftRight}
        style={{position: 'absolute',top: '0', left: '0', width: WIDTH, height: HEIGHT}}
    />
    return <div style={{marginBottom: "200px"}}>
        <h2>Indoor Navigator der FH Wedel</h2>
        <div >
            {webcam}    
        </div>
       <div style={{width: '180px', margin: 'auto'}}>
        <Select 
            options={options}
            onChange={(val) => onChangeSelect(val)}
        />
       </div>
        
        {isGoal  
            ? <div> Ziel erreicht </div>
            : <NavInfo currDir={currDir} nextDir={nextDir} dist={dist} 
        />}

    </div >
}

export default Navigation