/**
 * @file Experience.jsx
 * 
 *  
 */

import { Perf } from 'r3f-perf'
import { useGLTF, useAnimations } from '@react-three/drei'
import { useControls } from 'leva'
import { OrbitControls } from '@react-three/drei'
import MmaFighter from './MmaFighter.jsx'
import { useRef } from 'react'
import particlesVertexShader from './shaders/particles/vertex.glsl'
import particlesFragmentShader from './shaders/particles/fragment.glsl'
import * as THREE from 'three'

export default function Experience()
{
    const sizes = {
        width: window.innerWidth,
        height: window.innerHeight,
        pixelRatio: Math.min(window.devicePixelRatio, 2)
    }

    const { performance } = useControls('perf', { 
        performance: false 
    })

    const fighter1 = useRef()

    const { directionalLightIntensity, directionalLightPosition, ambientLightIntensity } =  useControls("Lighting",{
        directionalLightIntensity: {
            value: 2,
            min: 0,
            max: 20,
            step: 0.1
        },
        directionalLightPosition: {
            value: [0, 1, 0],
            step: 0.1
        },
        ambientLightIntensity: {
            value: 0.0,
            min: 0,
            max: 1,
            step: 0.1
        },
    })

    const { particles } = useControls('Particles', {
        colorA: '#ff0000',
        colorB: '#0000ff'
    })


    return <>

        {performance ? <Perf position='top-left'/> : null}

        <OrbitControls />

        <ambientLight 
            intensity={ambientLightIntensity}
        />
        <directionalLight
            position={directionalLightPosition}
            intensity={directionalLightIntensity}
        />
        <MmaFighter 
            color={'#ff0000'}
            position={[-1, 0, 0]}
        />
        <MmaFighter 
            color={'#ff0000'}
            position={[-1, 0, 0]}
        />
        <primitive object={MmaFighter} ref={fighter1} />
    </>
   
}