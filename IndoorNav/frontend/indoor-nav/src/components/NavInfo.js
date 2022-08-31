import { CaretDownOutlined, CaretLeftOutlined, CaretRightOutlined} from '@ant-design/icons';


function NavInfo({currDir, nextDir, dist}) {
    let iconDown = <CaretDownOutlined />
    let iconLeft = <CaretLeftOutlined />
    let iconRight = <CaretRightOutlined />

    const calcNavInfos = () => {
        if(currDir === 'down'){
            return <div>{iconDown} Umdrehen</div>
        }
        else  {
            if(nextDir === 'left'){
                return <div>{iconLeft} in {dist} Metern</div>
            } else if( nextDir === 'right'){
                return <div>{iconRight} in {dist} Metern</div>
            }  
        } 
    }

    return currDir && nextDir && dist ? calcNavInfos(): 'Keine Navigationsinformation'
}

export default NavInfo