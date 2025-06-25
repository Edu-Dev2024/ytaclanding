import * as THREE from 'three';

export class Bird {
  constructor() {
    this.velocity = 0;
    this.gravity = -15;
    this.flapStrength = 6;
    this.maxVelocity = 8;
    this.startPosition = new THREE.Vector3(0, 0, 0);
    
    this.createBird();
    this.reset();
  }
  
  createBird() {
    // Create bird group
    this.mesh = new THREE.Group();
    
    // Bird body (yellow)
    const bodyGeometry = new THREE.SphereGeometry(0.4, 16, 16);
    const bodyMaterial = new THREE.MeshLambertMaterial({ 
      color: 0xFFD700,
      flatShading: false
    });
    this.body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    this.body.castShadow = true;
    this.mesh.add(this.body);
    
    // Bird beak (orange)
    const beakGeometry = new THREE.ConeGeometry(0.1, 0.3, 8);
    const beakMaterial = new THREE.MeshLambertMaterial({ color: 0xFF8C00 });
    this.beak = new THREE.Mesh(beakGeometry, beakMaterial);
    this.beak.position.set(0.3, 0.1, 0);
    this.beak.rotation.z = -Math.PI / 2;
    this.mesh.add(this.beak);
    
    // Bird eyes
    const eyeGeometry = new THREE.SphereGeometry(0.08, 8, 8);
    const eyeMaterial = new THREE.MeshLambertMaterial({ color: 0x000000 });
    
    this.leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    this.leftEye.position.set(0.2, 0.2, 0.15);
    this.mesh.add(this.leftEye);
    
    this.rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    this.rightEye.position.set(0.2, 0.2, -0.15);
    this.mesh.add(this.rightEye);
    
    // Wings
    const wingGeometry = new THREE.EllipseCurve(0, 0, 0.3, 0.15, 0, 2 * Math.PI, false, 0);
    const wingPoints = wingGeometry.getPoints(16);
    const wingShape = new THREE.Shape(wingPoints);
    const wingExtrudeGeometry = new THREE.ExtrudeGeometry(wingShape, {
      depth: 0.05,
      bevelEnabled: false
    });
    const wingMaterial = new THREE.MeshLambertMaterial({ color: 0xFFB347 });
    
    this.leftWing = new THREE.Mesh(wingExtrudeGeometry, wingMaterial);
    this.leftWing.position.set(-0.1, 0, 0.25);
    this.leftWing.rotation.y = Math.PI / 6;
    this.mesh.add(this.leftWing);
    
    this.rightWing = new THREE.Mesh(wingExtrudeGeometry, wingMaterial);
    this.rightWing.position.set(-0.1, 0, -0.25);
    this.rightWing.rotation.y = -Math.PI / 6;
    this.mesh.add(this.rightWing);
    
    // Animation properties
    this.wingFlapTimer = 0;
    this.wingFlapSpeed = 8;
  }
  
  flap() {
    this.velocity = this.flapStrength;
    
    // Wing flap animation
    this.wingFlapTimer = 0.2;
  }
  
  update(deltaTime) {
    // Apply gravity
    this.velocity += this.gravity * deltaTime;
    
    // Clamp velocity
    this.velocity = Math.max(-this.maxVelocity, Math.min(this.maxVelocity, this.velocity));
    
    // Update position
    this.mesh.position.y += this.velocity * deltaTime;
    
    // Rotate bird based on velocity
    const rotationAngle = THREE.MathUtils.clamp(this.velocity * 0.1, -0.5, 0.5);
    this.mesh.rotation.z = rotationAngle;
    
    // Wing flap animation
    if (this.wingFlapTimer > 0) {
      this.wingFlapTimer -= deltaTime;
      const flapIntensity = this.wingFlapTimer / 0.2;
      
      this.leftWing.rotation.z = Math.sin(this.wingFlapTimer * this.wingFlapSpeed) * 0.5 * flapIntensity;
      this.rightWing.rotation.z = -Math.sin(this.wingFlapTimer * this.wingFlapSpeed) * 0.5 * flapIntensity;
    } else {
      // Gentle idle wing movement
      this.leftWing.rotation.z = Math.sin(Date.now() * 0.003) * 0.1;
      this.rightWing.rotation.z = -Math.sin(Date.now() * 0.003) * 0.1;
    }
    
    // Slight bobbing animation
    this.body.position.y = Math.sin(Date.now() * 0.005) * 0.02;
  }
  
  reset() {
    this.mesh.position.copy(this.startPosition);
    this.mesh.rotation.z = 0;
    this.velocity = 0;
    this.wingFlapTimer = 0;
  }
}