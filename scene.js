import * as THREE from 'three';

export class SceneManager {
  constructor(scene) {
    this.scene = scene;
    this.setupLighting();
    this.createBackground();
    this.createGround();
  }
  
  setupLighting() {
    // Bright ambient light to match the cheerful image
    const ambientLight = new THREE.AmbientLight(0x87CEEB, 0.6);
    this.scene.add(ambientLight);
    
    // Warm directional light
    const directionalLight = new THREE.DirectionalLight(0xFFE5B4, 1.0);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 50;
    directionalLight.shadow.camera.left = -20;
    directionalLight.shadow.camera.right = 20;
    directionalLight.shadow.camera.top = 20;
    directionalLight.shadow.camera.bottom = -20;
    this.scene.add(directionalLight);
  }
  
  createBackground() {
    // Create a bright cyan background to match the image
    this.scene.background = new THREE.Color(0x4FC3F7);
    
    // Add some distant mountains
    const mountainGeometry = new THREE.ConeGeometry(4, 8, 8);
    const mountainMaterial = new THREE.MeshLambertMaterial({ 
      color: 0x81C784,
      transparent: true,
      opacity: 0.7
    });
    
    // Create several mountains in the background
    for (let i = 0; i < 5; i++) {
      const mountain = new THREE.Mesh(mountainGeometry, mountainMaterial);
      mountain.position.set(
        (Math.random() - 0.5) * 40,
        -2,
        -25 + (Math.random() - 0.5) * 10
      );
      mountain.scale.set(
        0.5 + Math.random() * 0.5,
        0.5 + Math.random() * 0.5,
        0.5 + Math.random() * 0.5
      );
      this.scene.add(mountain);
    }
    
    // Add some floating clouds
    this.clouds = [];
    for (let i = 0; i < 6; i++) {
      const cloudGroup = new THREE.Group();
      
      // Create cloud using multiple spheres
      for (let j = 0; j < 3; j++) {
        const cloudGeometry = new THREE.SphereGeometry(0.5 + Math.random() * 0.3, 8, 8);
        const cloudMaterial = new THREE.MeshLambertMaterial({ 
          color: 0xFFFFFF,
          transparent: true,
          opacity: 0.8
        });
        const cloudSphere = new THREE.Mesh(cloudGeometry, cloudMaterial);
        cloudSphere.position.set(
          (Math.random() - 0.5) * 2,
          (Math.random() - 0.5) * 0.5,
          (Math.random() - 0.5) * 0.5
        );
        cloudGroup.add(cloudSphere);
      }
      
      cloudGroup.position.set(
        (Math.random() - 0.5) * 30,
        3 + Math.random() * 2,
        -15 + (Math.random() - 0.5) * 10
      );
      
      this.clouds.push({
        group: cloudGroup,
        speed: 0.1 + Math.random() * 0.2
      });
      
      this.scene.add(cloudGroup);
    }
  }
  
  createGround() {
    // Create ground plane
    const groundGeometry = new THREE.PlaneGeometry(100, 100);
    const groundMaterial = new THREE.MeshLambertMaterial({ 
      color: 0xDEB887,
      side: THREE.DoubleSide
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -4;
    ground.receiveShadow = true;
    this.scene.add(ground);
    
    // Add some ground decorations
    const decorationGeometry = new THREE.CylinderGeometry(0.1, 0.15, 0.3, 8);
    const decorationMaterial = new THREE.MeshLambertMaterial({ color: 0x8BC34A });
    
    for (let i = 0; i < 20; i++) {
      const decoration = new THREE.Mesh(decorationGeometry, decorationMaterial);
      decoration.position.set(
        (Math.random() - 0.5) * 40,
        -3.85,
        (Math.random() - 0.5) * 40
      );
      decoration.castShadow = true;
      this.scene.add(decoration);
    }
  }
  
  update(deltaTime) {
    // Animate clouds
    for (const cloud of this.clouds) {
      cloud.group.position.x -= cloud.speed * deltaTime;
      
      // Reset cloud position when it goes too far
      if (cloud.group.position.x < -20) {
        cloud.group.position.x = 20;
      }
    }
  }
}