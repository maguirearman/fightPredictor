/**
 * @file Experience.jsx
 * 
 *  
 */

import { Perf } from 'r3f-perf'
import { useGLTF, useAnimations } from '@react-three/drei'
import { useControls } from 'leva'
import { OrbitControls } from '@react-three/drei'
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

    const fighter = useGLTF('/models/fbxFighter.glb')
    console.log(fighter)
    const { actions } = useAnimations(fighter.animations)
    console.log(actions)

    const fighterGeometry = fighter.scene.children[0].children[0].geometry

    const { performance } = useControls('perf', { 
        performance: false 
    })

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

        <points
            position={[-3, -5, 0]}
            rotation={[Math.PI * 0.5, 0, -Math.PI * 0.5]}
            scale={[0.04, 0.04, 0.04]}
        >
            <primitive object={fighterGeometry} />
            <pointsMaterial
                size={0.02}
                sizeAttenuation={true}
                // depthTest={false}
                color={0xff0000}
            />
        </points>
        <points
            position={[3, -5., 0]}
            scale={[0.04, 0.04, 0.04]}
            rotation={[Math.PI * 0.5, 0, Math.PI * 0.5]}
        >
            <primitive object={fighterGeometry} />
            <pointsMaterial
                size={0.03}
                sizeAttenuation={true}
                // depthTest={false}
                color={0x0000ff}
            />
        </points>
    </>
   
}