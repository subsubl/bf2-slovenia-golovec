
Shaders
=======

This section provides a comprehensive reference and detailed descriptions for various shader files utilized in Project Reality, covering their functions in rendering graphics, effects, and environmental elements within the game.

.. object:: BundledMesh.fx

   Generates the shadow map for bundled mesh objects.

.. object:: CommonPixelLight.fxh

   Contains common pixel lighting functions used across multiple shaders.

.. object:: DebugCircleShader.fx

   This shader renders a circle for debugging purposes.

.. object:: DebugD3DXMeshShapeShader.fx

   Debug shader for rendering D3DX mesh shapes.

.. object:: DebugLineGraph.fx

   Renders line graphs for debugging visualization.

.. object:: DebugSphereShader.fx

   Debug shader for rendering sphere shapes.

.. object:: Decals.fx

   Handles decal rendering for surface details and effects.

.. object:: Font.fx

   Shader for rendering text and font elements.

.. object:: FSQuadDrawer.fx

   Full-screen quad drawer shader for post-processing effects including blurs and texture conversions.

.. object:: FXCommon.fxh

   This header file contains shared code and functions for particle shaders. It provides common utilities, parameters, and helper functions used across various particle and effect shaders in the system.

.. object:: LightGeom.fx

   Handles geometry lighting calculations.

.. object:: Lightning.fx

   Renders lightning effects and electrical discharges.

.. object:: LoadingScreen.fx

   Shader for rendering loading screen elements.

.. object:: MeshParticleMesh.fx

   Handles mesh-based particle system rendering.

.. object:: Nametag.fx

   Renders nametags and UI elements above objects.

.. object:: NonScreenAlignedParticles.fx

   Handles particle systems that are not screen-aligned.

.. object:: Particles.fx

   Main particle system shader for various effects.

.. object:: PortedFontShader.fx

   Ported font rendering shader.

.. object:: PortedMenuShader.fx

   Ported menu system shader.

.. object:: PostProduction_nv3x.fx

   This shader controls post-production effects including tinnitus and other screen-space effects. It handles various post-processing techniques to enhance visual quality and create special effects.

.. object:: RaCommon.fxh

   This header file provides common functions and definitions used across Reality shaders. It includes shared utilities, mathematical operations, and fundamental shader components that form the foundation of the rendering system.

.. object:: RaDefines.fx

   Defines common constants and macros used across various shaders.

.. object:: Rain.fx

   This shader renders rain effects with dynamic particle systems and environmental interactions. It handles rain droplet rendering, splash effects, and integration with the scene's lighting and fog systems.

.. object:: RaShader1Dif.fx

   This shader renders an object's diffuse map with basic lighting and fog effects. It handles simple diffuse texturing for objects and applies SRGB color space conversions and tonemaping.

.. object:: RaShader1Dif1BoneSkinned.fx

   This shader renders an object's diffuse map with bone-skinned animation support. It uses global variables to hold the view matrix, projection matrix, ambient material, diffuse material, and the light vector that describes the direction to the light source. The application initializes these variables.

.. object:: RaShaderBM.fx

   This shader renders lighting for bundled mesh (dynamic, non-human objects) and calculates world-space lighting with support for various features like normal mapping, GI maps, environment maps, UV animation, and shadow mapping. It handles bone-based animation and complex material properties.

.. object:: RaShaderBM.fxh

   This header file provides data structures and parameters for the RaShaderBM shader. It includes bone matrices, lighting parameters, material properties, and sampler definitions for bundled mesh rendering.

.. object:: RaShaderBM.mfx

   Configures the MetaFx for BundledMesh objects.

.. object:: RaShaderBMadditive.fx

   This shader renders additive lighting for bundled mesh (dynamic, non-human objects).

.. object:: RaShaderBMZOnly.fx

   This is a Z-only shader for bundled mesh (dynamic, non-human objects), which only writes to the depth buffer.

.. object:: RaShaderDefault.fx

   This basic shader outputs a solid color and serves as a fallback or default rendering shader. It handles simple vertex transformation and applies a fixed color output with depth writing support.

.. object:: RaShaderEditorRoad.fx

   This shader renders roads in the editor with basic diffuse and lightmap support. It handles road surface rendering with optional detail textures and applies fog effects based on camera distance. The shader includes special handling for road depth and Z-fading effects.

.. object:: RaShaderEditorRoadDetail.fx

   This shader renders roads with detail textures in the editor, building upon RaShaderEditorRoad.fx with additional detail texture support.

.. object:: RaShaderEditorRoadDetailNoBlend.fx

   This shader renders roads with detail textures in the editor without texture blending, building upon RaShaderEditorRoad.fx with detail texture support and disabled blending.

.. object:: RaShaderLeaf.fx

   This shader renders objects with leaf-like characteristics, including foliage and overgrowth. It handles wind animation for leaves, dynamic lighting with shadow support, and specialized alpha testing for foliage rendering. The shader includes features for both regular leaf objects and overgrowth patches.

.. object:: RaShaderLeafOG.fx

   This shader renders overgrowth leaf objects with enhanced foliage rendering features, building upon RaShaderLeaf.fx with overgrowth-specific functionality.

.. object:: RaShaderLeafPointLight.fx

   This shader renders leaf objects with dynamic point light illumination support, building upon RaShaderLeaf.fx with enhanced lighting calculations.

.. object:: RaShaderLeafPointLightShadowed.fx

   This shader renders leaf objects with point light illumination and shadow mapping support, building upon RaShaderLeafPointLight.fx with shadow rendering capabilities.

.. object:: RaShaderLeafShadowed.fx

   This shader renders leaf objects with shadow mapping support, building upon RaShaderLeaf.fx with enhanced shadow rendering capabilities.

.. object:: RaShaderRoad.fx

   This shader renders roads in the game with diffuse and detail texture support. It handles road surface rendering with lightmap accumulation, fog effects, and special Z-fading for road edges. The shader includes support for both basic roads and roads with detail textures.

.. object:: RaShaderRoadDetail.fx

   This shader renders roads with detail textures in the game, building upon RaShaderRoad.fx with additional detail texture support for enhanced road surface rendering.

.. object:: RaShaderRoadDetailNoBlend.fx

   This shader renders roads with detail textures in the game without texture blending, building upon RaShaderRoad.fx with detail texture support and disabled blending.

.. object:: RaShaderSM.fx

   This shader renders lighting for skinned mesh (dynamic, human-like objects with bones). It supports bone-based animation with 2-bone skinning, normal mapping, environment mapping, and shadow mapping. The shader calculates world-space lighting and handles complex material properties for character rendering.

.. object:: RaShaderSM.fxh

   This header file provides data structures and parameters for the RaShaderSM shader. It includes bone matrices, lighting parameters, material properties, and sampler definitions for skinned mesh rendering.

.. object:: RaShaderSM.mfx

   Configures the MetaFx for SkinnedMesh objects.

.. object:: RaShaderSTM.fx

   This shader renders lighting for static mesh (buildings, static props) and calculates tangent-space lighting. It supports multiple texture layers including base, detail, dirt, and crack maps, with optional parallax mapping and lightmap support. The shader handles complex material properties and surface details for static objects.

.. object:: RaShaderSTM.fxh

   This header file provides data structures and parameters for the RaShaderSTM shader. It includes material properties, texture sampling parameters, lighting constants, and sampler definitions for static mesh rendering with multiple texture layers.

.. object:: RaShaderSTM.mfx

   Configures the MetaFx for StaticMesh objects.

.. object:: RaShaderTrunkOG.fx

   This shader renders lighting for tree-trunk overgrowth objects. It handles specialized rendering for overgrowth tree trunks with dynamic lighting, fog effects, and LOD scaling. The shader is optimized for foliage and environmental objects.

.. object:: RaShaderTrunkSTMBase.fx

   This shader renders the base texture for static mesh tree trunks, focusing on the primary diffuse texture without additional detail layers.

.. object:: RaShaderTrunkSTMBaseShadowed.fx

   This shader renders the base texture for static mesh tree trunks with shadow mapping support, building upon RaShaderTrunkSTMBase.fx with enhanced shadow rendering capabilities.

.. object:: RaShaderTrunkSTMDetail.fx

   This shader renders lighting for objects with characteristics of tree-trunks (e.g., poles). It handles specialized rendering for trunk-like objects with diffuse and detail texture support, dynamic lighting, shadow mapping, and fog effects. The shader is optimized for environmental props and structural elements.

.. object:: RaShaderTrunkSTMDetailShadowed.fx

   This shader renders static mesh tree trunks with detail textures and shadow mapping support, building upon RaShaderTrunkSTMDetail.fx with enhanced shadow rendering capabilities.

.. object:: RaShaderWater2D.fx

   This shader renders 2D water surfaces with lightmap and shadow support, building upon RaShaderWaterBase.fx with enhanced lighting and shadow rendering capabilities.

.. object:: RaShaderWater3D.fx

   This shader renders 3D water surfaces with lightmap, shadow, and 3D texture support, building upon RaShaderWaterBase.fx with enhanced volumetric water rendering capabilities.

.. object:: RaShaderWaterBase.fx

   This shader renders water surfaces with dynamic lighting, reflection, and transparency effects. It supports environment mapping, lightmap accumulation, shadow mapping, and specialized water rendering techniques including Fresnel effects and depth-based transparency. The shader forms the base for various water rendering variants.

.. object:: RaShaderWaterDistant2D.fx

   This shader renders 2D water surfaces for distant viewing with lightmap support, building upon RaShaderWaterBase.fx with optimized rendering for distant water surfaces.

.. object:: RaShaderWaterDistant3D.fx

   This shader renders 3D water surfaces for distant viewing with lightmap and 3D texture support, building upon RaShaderWaterBase.fx with optimized volumetric rendering for distant water surfaces.

.. object:: RaShaderWaterHighEnd3D.fx

   This shader renders high-end 3D water surfaces with lightmap, shadow, and 3D texture support, building upon RaShaderWaterBase.fx with advanced volumetric water rendering capabilities.

.. object:: RaShaderWaterSurrounding2D.fx

   This shader renders 2D water surfaces for surrounding environmental areas, building upon RaShaderWaterBase.fx with optimized rendering for environmental water surfaces.

.. object:: RaShaderWaterSurrounding3D.fx

   This shader renders 3D water surfaces for surrounding environmental areas with volumetric texture support, building upon RaShaderWaterBase.fx with enhanced rendering for environmental water surfaces.

.. object:: RealityGraphics.fxh

   Core graphics functions and definitions for Reality engine.

.. object:: RoadCompiled.fx

   This shader renders lighting for compiled roads with texture blending and fade-out effects. It handles road surface rendering with specialized shaders for pre-compiled road geometry and applies distance-based fading.

.. object:: SimpleAlphaBlendShader.fx

   This shader provides simple alpha blending functionality for transparent objects. It handles basic texture-based transparency with alpha blending and supports fundamental transparent rendering techniques.

.. object:: SkinnedMesh.fx

   This shader builds shadow maps for skinned mesh objects (dynamic, human-like objects with bones). It performs bone skinning for up to 2 bones and generates shadow data used by RaShaderSM.fx for final rendering.

.. object:: SkyDome.fx

   This shader renders sky and skybox environments with specialized depth handling. It creates atmospheric effects, sky gradients, and celestial bodies while using normal depth calculation for distant geometry.

.. object:: StaticMesh.fx

   This shader builds shadow maps for static mesh objects (buildings, static props). It generates shadow data that is used by RaShaderSTM.fx for final rendering of static objects in the scene.

.. object:: SwiffMenu.fx

   This shader contains rendering functions for the main menu interface. It handles UI element rendering, texture mapping, and visual effects specifically designed for menu systems and user interface components.

.. object:: TerrainShader_Hi.fxh

   This high-settings terrain shader renders terrain with advanced shading, shadowing, and detail features. It provides high-quality terrain rendering with multiple texture layers, normal mapping, and sophisticated lighting calculations.

.. object:: TerrainShader_Low.fxh

   This low-settings terrain shader renders terrain with optimized performance and reduced quality. It provides basic terrain rendering with simplified shading and shadowing for lower-end hardware or performance-critical scenarios.

.. object:: TerrainShader_Shared.fxh

   This header file contains shared functions and utilities for terrain shaders. It provides common terrain rendering components, lightmap generation, and helper functions used by both high and low detail terrain shaders.

.. object:: TerrainShader.fx

   This shader combines different parts of the terrain shader based on quality settings, integrating TerrainShader.fxh for core functionality and selecting between high and low quality implementations.

.. object:: TerrainShader.fxh

   This terrain shader renders lighting for ground terrain with comprehensive feature support. It handles terrain texture blending, lighting accumulation, shadow mapping, and environmental interactions for realistic ground rendering.

.. object:: Trail.fx

   This shader renders lighting for particles that emit smoke trails and other trail effects. It handles specialized particle rendering with Fresnel effects, transparency, and dynamic lighting for trail systems.

.. object:: Undergrowth.fx

   This shader renders lighting for undergrowth elements such as grass, bushes, and low vegetation. It handles specialized rendering for ground cover with wind animation, lighting, and optimized performance for dense vegetation.
