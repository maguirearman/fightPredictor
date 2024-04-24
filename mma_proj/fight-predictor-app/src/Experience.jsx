/**
 * @file Experience.jsx
 * 
 *  
 */

import { Perf } from 'r3f-perf'
import { useGLTF, MeshTransmissionMaterial, Center, useAnimations, useFBX } from '@react-three/drei'
import { useControls } from 'leva'
import { OrbitControls } from '@react-three/drei'

export default function Experience()
{

    const fighter = useFBX('/models/Boxing.fbx')
    console.log(fighter)




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

    const materialProps = useControls("Material", {
        color: '#ffffff',
        clearcoat: 1,
        transmission: 0.9,
        thickness: 0.1,
        ior: 1.5,
        roughness: 0.1,
        metalness: 0.1,
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

        <Center>
            <mesh>
                <primitive object={fighterGeometry} />
                <meshStandardMaterial
                    color={materialProps.color}
                    roughness={materialProps.roughness}
                    metalness={materialProps.metalness}
                />
            </mesh>
        </Center>
        
    </>
   
}