// InstancedSkinnedMeshComponent.jsx
import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { extend, useFrame, useThree } from '@react-three/fiber';
import { SkeletonHelper } from '@react-three/drei';
import { InstancedSkinnedMesh } from './InstancedSkinnedMesh'; // Adjust the import path as needed

// Extend R3F with the new class
extend({ InstancedSkinnedMesh });

const InstancedSkinnedMeshComponent = ({ geometry, material, skeleton, count = 1 }) => {
  const meshRef = useRef();
  const { scene } = useThree();

  useEffect(() => {
    if (meshRef.current) {
      // Set initial instance matrices and other properties if needed
      for (let i = 0; i < count; i++) {
        const dummy = new THREE.Object3D();
        dummy.position.set(i, 0, 0);
        dummy.updateMatrix();
        meshRef.current.setMatrixAt(i, dummy.matrix);
      }
      meshRef.current.instanceMatrix.needsUpdate = true;

      // Add SkeletonHelper to the scene
      const helper = new THREE.SkeletonHelper(meshRef.current);
      scene.add(helper);
    }
  }, [count, scene]);

  useFrame(() => {
    // Update logic if necessary
  });

  return (
    <instancedSkinnedMesh ref={meshRef} args={[geometry, material, count]}>
      <primitive object={skeleton} attach="skeleton" />
    </instancedSkinnedMesh>
  );
};

export default InstancedSkinnedMeshComponent;
