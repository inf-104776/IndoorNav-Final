import React, { useRef, useEffect } from 'react'

function drawArrow(ctx, fromx, fromy, tox, toy, size, arrowWidth, color){
    //variables to be used when creating the arrow
    var headlen = size;//10;
    var angle = Math.atan2(toy-fromy,tox-fromx);
 
    ctx.save();
    ctx.strokeStyle = color;
 
    //starting path of the arrow from the start square to the end square
    //and drawing the stroke
    ctx.beginPath();
    ctx.moveTo(fromx, fromy);
    ctx.lineTo(tox, toy);
    ctx.lineWidth = arrowWidth;
    ctx.stroke();
 
    //starting a new path from the head of the arrow to one of the sides of
    //the point
    ctx.beginPath();
    ctx.moveTo(tox, toy);
    ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
               toy-headlen*Math.sin(angle-Math.PI/7));
 
    //path from the side point of the arrow, to the other side point
    ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),
               toy-headlen*Math.sin(angle+Math.PI/7));
 
    //path from the side point back to the tip of the arrow, and then
    //again to the opposite side point
    ctx.lineTo(tox, toy);
    ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
               toy-headlen*Math.sin(angle-Math.PI/7));
 
    //draws the paths created above
    ctx.stroke();
    ctx.restore();
}

const draw = (ctx, markerDirUpDown, markerPosUpDown, markerDirLeftRight, markerPosLeftRight) => {
    if(markerPosLeftRight && markerDirLeftRight){
        let toPos = null

        if(markerDirLeftRight === "left"){
            toPos = [markerPosLeftRight[0] - 15, markerPosLeftRight[1]]
        } else if(markerDirLeftRight === "right"){
            toPos =  [markerPosLeftRight[0] + 15, markerPosLeftRight[1]]
        }
        let size = 5
        drawArrow(ctx, markerPosLeftRight[0], markerPosLeftRight[1], toPos[0], toPos[1], size, 3, 'white' )
    }
    
    if(markerPosUpDown && markerPosUpDown.length > 0 && markerDirUpDown ){      
        markerPosUpDown.sort(([a, b], [c, d]) => b - d);

        for (let i = 0; i < markerPosUpDown.length; i++){
            let size = i + 3
            let pos = markerPosUpDown[i]
            pos[1] -= 20
            let height = (i * 3) + 10         
            let toPos = [pos[0], pos[1] - height]
            drawArrow(ctx, pos[0], pos[1], toPos[0], toPos[1], size, 3,'white' )
        }   
    }
  }

const Canvas = ({ width, height, markerDirUpDown, markerPosUpDown, markerDirLeftRight, markerPosLeftRight }) => {
   
    const canvasRef = useRef(null)
  
    function resizeCanvasToDisplaySize(canvas) {
        canvas.width = width
        canvas.height = height
    }

    //component updates when one of markerDirUpDown, markerPosUpDown, 
    //markerDirLeftRight, markerPosLeftRight is updated
    useEffect(() => {
        const canvas = canvasRef.current
        const context = canvas.getContext('2d')
        resizeCanvasToDisplaySize(canvas)
        draw(context, markerDirUpDown, markerPosUpDown, markerDirLeftRight, markerPosLeftRight)
    }, [markerDirUpDown, markerPosUpDown, markerDirLeftRight, markerPosLeftRight])
  
    return <canvas ref={canvasRef} {...props}/>
}

export default Canvas