#NOTE: this abstraction allows for both the documentation to be centrally managed and inherited
from abc import ABCMeta
class NodeConfigMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if name in NODE_CONFIGS:
            for key, value in NODE_CONFIGS[name].items():
                setattr(new_class, key, value)
        return new_class

class CombinedMeta(NodeConfigMeta, ABCMeta):
    pass

def add_node_config(node_name, config):
    NODE_CONFIGS[node_name] = config

NODE_CONFIGS = {}

add_node_config("MaskBase", {
    "BASE_DESCRIPTION": """
##Parameters
- `Masks`: Input mask or sequence of masks to be processed. (you can pass in a blank mask if you want)
- `Strength`: Controls the intensity of the effect (0.0 to 1.0). Higher values make the mask operation more pronounced.
- `Invert`: When enabled, reverses the mask, turning black areas white and vice versa.
- `Subtract Original`: Removes a portion of the original mask from the result (0.0 to 1.0). Higher values create more pronounced edge effects.
- `Grow with Blur`: Expands the mask edges (0.0 to 10.0). Higher values create softer, more expanded edges.
"""
})

add_node_config("TemporalMaskBase", {
    "ADDITIONAL_INFO": """
- `Start Frame`: The frame number where the effect begins (0 to 1000).
- `End Frame`: The frame number where the effect ends (0 to 1000). If set to 0, continues until the last frame.
- `Effect Duration`: Number of frames over which the effect is applied (0 to 1000). If 0, uses (End Frame - Start Frame).
- `Temporal Easing`: Controls how the effect strength changes over time, affecting the smoothness of transitions.
  - Options: "ease_in_out", "linear", "bounce", "elastic", "none"
- `Palindrome`: When enabled, the effect plays forward then reverses within the specified duration, creating a back-and-forth motion.
"""
})

add_node_config("ParticleSystemMaskBase", {
    "ADDITIONAL_INFO": """
- `particle_count`: Total number of particles in the system (1 to 10000). More particles create denser effects.
- `particle_lifetime`: How long each particle exists in seconds (0.1 to 10.0). Longer lifetimes create more persistent effects.
- `wind_strength`: Power of the wind effect (-100.0 to 100.0). Positive values blow right, negative left.
- `wind_direction`: Angle of the wind in degrees (0.0 to 360.0). 0 is right, 90 is up, etc.
- `gravity`: Strength of downward pull (-1000.0 to 1000.0). Negative values make particles float up.
- `start_frame`: Frame to begin the particle effect (0 to 1000).
- `end_frame`: Frame to stop the particle effect (0 to 1000).
- `respect_mask_boundary`: When enabled, particles stay within the mask's shape.

Optional inputs:
- `emitters`: Particle emitter configurations (PARTICLE_EMITTER type). Define where particles originate.
- `vortices`: Optional vortex configurations (VORTEX type). Create swirling effects.
- `wells`: Optional gravity well configurations (GRAVITY_WELL type). Create areas that attract or repel particles.
- `well_strength_multiplier`: Amplifies the power of gravity wells (0.0 to 10.0). Higher values create stronger attraction/repulsion.
"""
})

add_node_config("ParticleEmissionMask", {
    "TOP_DESCRIPTION": "This is the main node for particle simulations. It creates dynamic, fluid-like effects through particle simulation. Supports multiple particle emitters, force fields (Gravity Well, Vortex), and allows for complex particle behaviors including boundary-respecting particles and static body interactions.",
    "ADDITIONAL_INFO": """
- `emission_strength`: Strength of particle emission effect (0.0 to 1.0), basically opacity
- `draw_modifiers`: Visibility of vortices and gravity wells (0.0 to 1.0)
"""
})

add_node_config("OpticalFlowMaskBase", {
    "ADDITIONAL_INFO": """
- `Images`: Input image sequence for optical flow calculation
- `Masks`: Input mask sequence to be processed
- `Strength`: Overall intensity of the effect (0.0 to 1.0). Higher values create more pronounced motion-based effects.
- `Flow Method`: Technique used for optical flow calculation. Each method has different speed/accuracy tradeoffs.
  - Options: "Farneback", "LucasKanade", "PyramidalLK"
- `Flow Threshold`: Minimum motion required to trigger the effect (0.0 to 1.0). Higher values ignore subtle movements.
- `Magnitude Threshold`: Relative threshold for flow magnitude (0.0 to 1.0). Higher values focus on areas of stronger motion.
"""
})

add_node_config("OpticalFlowMaskModulation", {
    "TOP_DESCRIPTION": "This is currently the main Optical Flow node. Use it to make motion based effects.",
    "ADDITIONAL_INFO": """
- `Modulation Strength`: Intensity of the modulation effect (0.0 to 5.0). Higher values create more pronounced motion trails.
- `Blur Radius`: Smoothing applied to the flow magnitude (0 to 20 pixels). Larger values create smoother trails.
- `Trail Length`: Number of frames for the trail effect (1 to 20). Longer trails last longer.
- `Decay Factor`: Rate of trail decay over time (0.1 to 1.0). Lower values make trails fade faster.
- `Decay Style`: Method of trail decay.
  - Options: "fade" (opacity reduction), "thickness" (width reduction)
- `Max Thickness`: Maximum trail thickness for thickness-based decay (1 to 50 pixels). Larger values create thicker trails.
"""
})

add_node_config("OpticalFlowDirectionMask", {
    "TOP_DESCRIPTION": "***WORK IN PROGRESS***"
})

add_node_config("OpticalFlowParticleSystem", {
    "TOP_DESCRIPTION": "***WORK IN PROGRESS***"
})

add_node_config("MaskTransform", {
    "TOP_DESCRIPTION": "Applies geometric transformations to the mask over time.",
    "ADDITIONAL_INFO": """
- `Transform Type`: The type of transformation to apply.
  - Options: "translate", "rotate", "scale"
- `X Value`: Horizontal component of the transformation (-1000 to 1000). Positive values move right, negative left.
- `Y Value`: Vertical component of the transformation (-1000 to 1000). Positive values move up, negative down.
"""
})

add_node_config("MaskMorph", {
    "TOP_DESCRIPTION": "Applies morphological operations to the mask, changing its shape over time.",
    "ADDITIONAL_INFO": """
- `Morph Type`: The type of morphological operation to apply.
  - Options: "erode", "dilate", "open", "close"
- `Max Kernel Size`: Maximum size of the morphological kernel (3 to 21, odd numbers only). Larger values create more pronounced effects.
- `Max Iterations`: Maximum number of times to apply the operation (1 to 50). More iterations create more extreme effects.
"""
})

add_node_config("MaskMath", {
    "TOP_DESCRIPTION": "Combines two masks using various mathematical operations.",
    "ADDITIONAL_INFO": """
- `Mask B`: Second mask to combine with the input mask.
- `Combination Method`: Mathematical operation to apply.
  - Options: "add", "subtract", "multiply", "minimum", "maximum"
"""
})

add_node_config("MaskRings", {
    "TOP_DESCRIPTION": "Creates concentric ring patterns based on the distance from the mask edges.",
    "ADDITIONAL_INFO": """
- `Num Rings`: Number of rings to generate (1 to 50). More rings create more detailed patterns.
- `Max Ring Width`: Maximum width of each ring as a fraction of the total distance (0.01 to 0.5). Larger values create wider rings.
"""
})

add_node_config("MaskWarp", {
    "TOP_DESCRIPTION": "Applies various warping effects to the mask, creating distortions and movement.",
    "ADDITIONAL_INFO": """
- `Warp Type`: The type of warping effect to apply. Each creates a different distortion pattern.
  - Options: "perlin" (noise-based), "radial" (circular), "swirl" (spiral)
- `Frequency`: Controls the scale of the warping effect (0.01 to 1.0). Higher values create more rapid changes in the warp pattern.
- `Amplitude`: Controls the strength of the warping effect (0.1 to 500.0). Higher values create more extreme distortions.
- `Octaves`: For noise-based warps, adds detail at different scales (1 to 8). More octaves create more complex, detailed patterns.
"""
})

add_node_config("BaseFeatureNode", {
    "BASE_DESCRIPTION": "Provides a foundation for creating features that control mask modulation. Features are used to dynamically adjust mask operations over time or based on various inputs."
})

add_node_config("MIDILoadAndExtract", {
    "TOP_DESCRIPTION": """
    Loads a MIDI file and extracts specified features for mask modulation. To use this, select the notes on the piano that you want to use to control modulations. 
    Many of the different types of information in the notes can be chosen as the driving feature.""",
    "ADDITIONAL_INFO": """
- `midi_file`: Path to the MIDI file to load and analyze
- `track_selection`: Which track(s) to analyze ("all" or specific track number)
- `attribute`: MIDI attribute to extract (e.g., "Note On/Off", "Pitchbend", "Pitch", "Aftertouch")
- `frame_rate`: Frame rate of the video to sync MIDI data with
- `video_frames`: Corresponding video frames (IMAGE type)
- `chord_only`: When true, only considers full chords (BOOLEAN)
- `notes`: Specific notes to consider (comma-separated string of MIDI note numbers, e.g., "60,64,67" for C major triad)
"""
})

add_node_config("AudioFilter", {
    "TOP_DESCRIPTION": "Applies frequency filters to audio for targeted sound processing.",
    "ADDITIONAL_INFO": """
- `audio`: Input audio to be filtered (AUDIO type)
- `filters`: Frequency filters to be applied (FREQUENCY_FILTER type). These determine which frequencies are emphasized or reduced.
"""
})

add_node_config("FrequencyFilterPreset", {
    "TOP_DESCRIPTION": "Creates preset filter chains for common audio processing tasks, simplifying complex audio manipulations.",
    "ADDITIONAL_INFO": """
- `preset`: Preset to use (e.g., "isolate_kick_drum" emphasizes low frequencies, "isolate_vocals" focuses on mid-range, "remove_rumble" cuts low frequencies)

Optional inputs:
- `previous_filter`: Previous filter chain to append to, allowing for cumulative effects
"""
})

add_node_config("FrequencyFilterCustom", {
    "TOP_DESCRIPTION": "Creates custom frequency filters.",
    "ADDITIONAL_INFO": """
- `filter_type`: Type of filter ("lowpass", "highpass", "bandpass")
- `order`: Filter order (1 to 10)
- `cutoff`: Cutoff frequency (20 to 20000 Hz)

Optional inputs:
- `previous_filter`: Previous filter chain to append to
"""
})

add_node_config("AudioFeatureVisualizer", {
    "TOP_DESCRIPTION": "***WORK IN PROGESS*** Visualizes various audio features, creating visual representations of sound characteristics.",
    "ADDITIONAL_INFO": """
- `audio`: Input audio to visualize (AUDIO type)
- `video_frames`: Corresponding video frames to overlay visualizations on (IMAGE type)
- `visualization_type`: Type of visualization to generate:
  - "waveform": Shows amplitude over time
  - "spectrogram": Displays frequency content over time
  - "mfcc": Mel-frequency cepstral coefficients, useful for speech recognition
  - "chroma": Represents pitch classes, useful for harmonic analysis
  - "tonnetz": Tonal space representation
  - "spectral_centroid": Shows the "center of mass" of the spectrum over time
- `frame_rate`: Frame rate of the video for synchronization
"""
})

add_node_config("AudioSeparator", {
    "TOP_DESCRIPTION": "Separates an input audio track into its component parts using the Open-Unmix model.",
    "ADDITIONAL_INFO": """
- `audio`: Input audio to be separated (AUDIO type)
- `video_frames`: Corresponding video frames (IMAGE type)
- `frame_rate`: Frame rate of the video for synchronization

Outputs:
- Original audio
- Isolated drums track
- Isolated vocals track
- Isolated bass track
- Isolated other instruments track
- FeaturePipe containing frame information

This node uses the Open-Unmix model to separate the input audio into four stems: drums, vocals, bass, and other instruments. Each separated track is returned as an individual AUDIO type output, along with the original audio and a FeaturePipe for further processing.
"""
})

add_node_config("SpringJointSetting", {
    "TOP_DESCRIPTION": "Defines the behavior of spring joints attached to particles.",
    "ADDITIONAL_INFO": """
- `stiffness`: Stiffness of the spring (0.0 to 1000.0). Higher values create stronger connections.
- `damping`: Damping factor of the spring (0.0 to 100.0). Higher values create more resistance to motion.
- `rest_length`: Rest length of the spring (0.0 to 100.0). Longer springs allow for more stretching.
- `max_distance`: Maximum distance the spring can stretch (0.0 to 500.0). Larger values allow for more elasticity.
"""
})

add_node_config("StaticBody", {
    "TOP_DESCRIPTION": "Defines static bodies in the simulation that particles can interact with (think walls, barrier, ramps, etc.).",
    "ADDITIONAL_INFO": """
- `shape_type`: Type of shape ("segment" or "polygon")
- `x1`, `y1`, `x2`, `y2`: Coordinates defining the shape
- `elasticity`: Bounciness of the static body (0.0 to 1.0). Higher values create more bouncy collisions.
- `friction`: Friction of the static body (0.0 to 1.0). Higher values create more resistance to motion.
- `draw`: Whether to visualize the static body and how thick
- `color`: Color of the static body (RGB tuple)
"""
})

add_node_config("GravityWell", {
    "TOP_DESCRIPTION": "An optional input for a simulation space. These can be chained together to add many to a simulation.",
    "ADDITIONAL_INFO": """
- `x`: X-coordinate of the gravity well (0.0 to 1.0)
- `y`: Y-coordinate of the gravity well (0.0 to 1.0)
- `strength`: Strength of the gravity well. Higher values create stronger attraction or repulsion.
- `radius`: Radius of effect for the gravity well. Larger values affect a wider area.
- `type`: Type of gravity well ('attract' or 'repel'). Attract pulls particles in, repel pushes them away.
- `color`: Color of the gravity well visualization (RGB tuple)
- `draw`: Thickness of the gravity well visualization (0.0 to 1.0)
"""
})

add_node_config("Vortex", {
    "TOP_DESCRIPTION": "An optional input for a simulation space. These can be chained together to add many to a simulation",
    "ADDITIONAL_INFO": """
- `x`: X-coordinate of the vortex center (0.0 to 1.0)
- `y`: Y-coordinate of the vortex center (0.0 to 1.0)
- `strength`: Strength of the vortex effect (0.0 to 1000.0). Higher values create stronger swirling motion.
- `radius`: Radius of effect for the vortex (10.0 to 500.0). Larger values create wider swirling areas.
- `inward_factor`: Factor controlling how quickly particles are pulled towards the center (0.0 to 1.0). Higher values create tighter spirals.
- `movement_speed`: Speed of movement of the vortex object (0.0 to 10.0). Higher values make the vortex move faster in the simulation space.
- `color`: Color of the vortex visualization (RGB tuple)
- `draw`: Thickness of the vortex visualization (0.0 to 1.0)
"""
})

add_node_config("ParticleModulationBase", {
    "TOP_DESCRIPTION": "Base class for particle modulation settings.",
    "ADDITIONAL_INFO": """
- `start_frame`: Frame to start the modulation effect (0 to 1000)
- `end_frame`: Frame to end the modulation effect (0 to 1000)
- `effect_duration`: Duration of the modulation effect in frames (0 to 1000)
- `temporal_easing`: Easing function for the modulation effect ("ease_in_out", "linear", "bounce", "elastic", "none")
- `palindrome`: Whether to reverse the modulation effect after completion (True/False)
"""
})

add_node_config("ParticleSizeModulation", {
    "TOP_DESCRIPTION": "Modulates particle size over time.",
    "ADDITIONAL_INFO": """
- `target_size`: Target size for particles at the end of the modulation (0.0 to 400.0)
"""
})

add_node_config("ParticleSpeedModulation", {
    "TOP_DESCRIPTION": "Modulates particle speed over time.",
    "ADDITIONAL_INFO": """
- `target_speed`: Target speed for particles at the end of the modulation (0.0 to 1000.0)
"""
})

add_node_config("ParticleColorModulation", {
    "TOP_DESCRIPTION": "Modulates particle color over time.",
    "ADDITIONAL_INFO": """
- `target_color`: Target color for particles at the end of the modulation (RGB tuple)
"""
})

add_node_config("FlexMaskBase", {
    "BASE_DESCRIPTION": """
Provides a base for mask operations modulated by various features.

## Common Parameters
- `feature`: The feature used to modulate the mask operation (FEATURE type)
- `feature_pipe`: The feature pipe containing frame information (FEATURE_PIPE type)
- `feature_threshold`: Threshold for feature activation (0.0 to 1.0)

Optional inputs:
- `feature`: The feature used to modulate the mask operation (FEATURE type)
- `feature_pipe`: The feature pipe containing frame information (FEATURE_PIPE type)
"""
})

add_node_config("FlexMaskMorph", {
    "TOP_DESCRIPTION": "Applies morphological operations to the mask, modulated by a selected feature.",
    "ADDITIONAL_INFO": """
- `morph_type`: The type of morphological operation to apply.
  - Options: "erode", "dilate", "open", "close"
- `max_kernel_size`: Maximum size of the morphological kernel (3 to 21, odd numbers only). Larger values create more pronounced effects.
- `max_iterations`: Maximum number of times to apply the operation (1 to 50). More iterations create more extreme effects.

The strength of the morphological operation is determined by the selected feature's value at each frame.
"""
})

add_node_config("FlexMaskWarp", {
    "TOP_DESCRIPTION": "Applies warping effects to the mask, modulated by a selected feature.",
    "ADDITIONAL_INFO": """
- `warp_type`: The type of warping effect to apply. Each creates a different distortion pattern.
  - Options: "perlin" (noise-based), "radial" (circular), "swirl" (spiral)
- `frequency`: Controls the scale of the warping effect (0.01 to 1.0). Higher values create more rapid changes in the warp pattern.
- `max_amplitude`: Maximum amplitude of the warping effect (0.1 to 500.0). Higher values create more extreme distortions.
- `octaves`: For noise-based warps, adds detail at different scales (1 to 8). More octaves create more complex, detailed patterns.

The intensity of the warping effect is determined by the selected feature's value at each frame.
"""
})

add_node_config("FlexMaskTransform", {
    "TOP_DESCRIPTION": "Applies geometric transformations to the mask, modulated by a selected feature.",
    "ADDITIONAL_INFO": """
- `transform_type`: The type of transformation to apply.
  - Options: "translate", "rotate", "scale"
- `max_x_value`: Maximum horizontal component of the transformation (-1000.0 to 1000.0). Positive values move right, negative left.
- `max_y_value`: Maximum vertical component of the transformation (-1000.0 to 1000.0). Positive values move up, negative down.

The extent of the transformation is determined by the selected feature's value at each frame.
"""
})

add_node_config("FlexMaskMath", {
    "TOP_DESCRIPTION": "Performs mathematical operations between two masks, modulated by a selected feature.",
    "ADDITIONAL_INFO": """
- `mask_b`: Second mask to combine with the input mask.
- `combination_method`: Mathematical operation to apply.
  - Options: "add", "subtract", "multiply", "minimum", "maximum"

The strength of the combination is determined by the selected feature's value at each frame.
"""
})

add_node_config("BaseFeatureNode", {
    "BASE_DESCRIPTION": """
 Features are used to modulate mask operations in FlexMask nodes.

## Common Parameters
- `frame_rate`: Frame rate of the video
- `frame_count`: Total number of frames
"""
})

add_node_config("TimeFeatureNode", {
    "TOP_DESCRIPTION": "Produces a feature that changes over time based on the selected effect type. This can be used to create dynamic, time-varying mask modulations.",
    "ADDITIONAL_INFO": """
- `effect_type`: Type of time-based pattern to apply.
  - Options: "smooth" (gradual), "accelerate" (speeds up), "pulse" (rhythmic), "sawtooth" (repeating ramp), "bounce" (up and down)
- `speed`: How quickly the effect progresses (0.1 to 10.0, default: 1.0). Higher values create faster changes.
- `offset`: Shifts the starting point of the effect (0.0 to 1.0, default: 0.0). Useful for staggering multiple effects.


"""
})

add_node_config("AudioFeatureNode", {
    "TOP_DESCRIPTION": "Analyzes the input audio to extract the specified feature. This feature can then be used to modulate masks based on audio characteristics.",
    "ADDITIONAL_INFO": """
- `audio`: Input audio to analyze (AUDIO type)
- `feature_type`: Type of audio feature to extract.
  - Options: "amplitude_envelope", "rms_energy", "spectral_centroid", "onset_detection", "chroma_features"

"""
})

add_node_config("DepthFeatureNode", {
    "TOP_DESCRIPTION": "Analyzes the input depth maps to extract the specified depth-related feature. This feature can be used to modulate masks based on depth information in the scene.",
    "ADDITIONAL_INFO": """
- `depth_maps`: Input depth maps to analyze (IMAGE type)
- `feature_type`: Type of depth feature to extract.
  - Options: "mean_depth", "depth_variance", "depth_range", "gradient_magnitude", "foreground_ratio", "midground_ratio", "background_ratio"

"""
})

add_node_config("ColorFeatureNode", {
    "TOP_DESCRIPTION": "Extracts color-related features from video frames for mask modulation.",
    "ADDITIONAL_INFO": """
- `feature_type`: Type of color feature to extract
  - Options: "dominant_color" (most prevalent color), "color_variance" (variation in colors), "saturation" (color intensity), "red_ratio" (proportion of red), "green_ratio" (proportion of green), "blue_ratio" (proportion of blue)

Analyzes the input video frames to extract the specified color-related feature. This feature can be used to modulate masks based on color information in the scene, creating effects that respond to color changes over time.
"""
})

add_node_config("BrightnessFeatureNode", {
    "TOP_DESCRIPTION": "Extracts brightness-related features from video frames for mask modulation.",
    "ADDITIONAL_INFO": """
- `feature_type`: Type of brightness feature to extract
  - Options: "mean_brightness" (average brightness), "brightness_variance" (variation in brightness), "dark_ratio" (proportion of dark areas), "mid_ratio" (proportion of mid-tone areas), "bright_ratio" (proportion of bright areas)

Analyzes the input video frames to extract the specified brightness-related feature. This feature can be used to modulate masks based on lighting changes in the scene, allowing for effects that respond to overall brightness or specific tonal ranges.
"""
})

add_node_config("MotionFeatureNode", {
    "TOP_DESCRIPTION": "Extracts motion-related features from video frames for mask modulation.",
    "ADDITIONAL_INFO": """
- `feature_type`: Type of motion feature to extract
  - Options: "mean_motion" (average motion), "max_motion" (peak motion), "motion_direction" (overall direction), "horizontal_motion" (left-right movement), "vertical_motion" (up-down movement), "motion_complexity" (intricacy of motion)
- `flow_method`: Technique used for optical flow calculation
  - Options: "Farneback" (dense flow), "LucasKanade" (sparse flow), "PyramidalLK" (multi-scale sparse flow)
- `flow_threshold`: Minimum motion magnitude to consider (0.0 to 10.0). Higher values ignore subtle movements.
- `magnitude_threshold`: Relative threshold for motion magnitude (0.0 to 1.0). Higher values focus on areas of stronger motion.

Analyzes the input video frames to extract the specified motion-related feature using optical flow techniques. This feature can be used to modulate masks based on movement in the scene, creating effects that respond to motion intensity, direction, or complexity.
"""
})

add_node_config("AudioFeatureExtractor", {
    "TOP_DESCRIPTION": "Analyzes the input audio to extract the specified feature. The resulting feature can be used to modulate masks based on audio characteristics.",
    "ADDITIONAL_INFO": """
- `audio`: Input audio to analyze (AUDIO type)
- `feature_pipe`: Feature pipe for frame information (FEATURE_PIPE type)
- `feature_type`: Type of audio feature to extract
  - Options: "amplitude_envelope", "rms_energy", "spectral_centroid", "onset_detection", "chroma_features"

"""
})

add_node_config("TimeFeatureNode", {
    "TOP_DESCRIPTION": "Generates time-based features for mask modulation.",
    "ADDITIONAL_INFO": """
- `video_frames`: Input video frames (IMAGE type)
- `frame_rate`: Frame rate of the video
- `effect_type`: Type of time-based pattern to apply
  - Options: "smooth" (gradual), "accelerate" (speeds up), "pulse" (rhythmic), "sawtooth" (repeating ramp), "bounce" (up and down)
- `speed`: How quickly the effect progresses (0.1 to 10.0, default: 1.0). Higher values create faster changes.
- `offset`: Shifts the starting point of the effect (0.0 to 1.0, default: 0.0). Useful for staggering multiple effects.

Generates a feature that changes over time based on the selected effect type. This can be used to create dynamic, time-varying mask modulations.
"""
})

add_node_config("DepthFeatureNode", {
    "TOP_DESCRIPTION": "Extracts depth-related features from depth maps for mask modulation.",
    "ADDITIONAL_INFO": """
- `video_frames`: Input video frames (IMAGE type)
- `frame_rate`: Frame rate of the video
- `depth_maps`: Input depth maps to analyze (IMAGE type)
- `feature_type`: Type of depth feature to extract
  - Options: "mean_depth", "depth_variance", "depth_range", "gradient_magnitude", "foreground_ratio", "midground_ratio", "background_ratio"

Analyzes the input depth maps to extract the specified depth-related feature. This feature can be used to modulate masks based on depth information in the scene.
"""
})

add_node_config("EmitterMovement", {
    "TOP_DESCRIPTION": """These parameters work together to create complex, periodic movements for particle emitters. 
By adjusting frequencies and amplitudes, you can achieve various patterns like circles, 
figure-eights, or more chaotic motions. The direction parameters add extra dynamism by 
altering the angle of particle emission over time.""",
    "ADDITIONAL_INFO": """
Position Control:
- `emitter_x_frequency`: How quickly the emitter moves horizontally (0.0 to 10.0). Higher values create faster side-to-side motion.
- `emitter_x_amplitude`: Maximum horizontal distance the emitter moves (0.0 to 0.5). Larger values create wider movements.
- `emitter_y_frequency`: How quickly the emitter moves vertically (0.0 to 10.0). Higher values create faster up-and-down motion.
- `emitter_y_amplitude`: Maximum vertical distance the emitter moves (0.0 to 0.5). Larger values create taller movements.
Direction Control:
- `direction_frequency`: How quickly the emission angle changes (0.0 to 10.0). Higher values create more rapid direction changes.
- `direction_amplitude`: Maximum angle change in degrees (0.0 to 180.0). Larger values allow for more extreme direction shifts.


"""
})

add_node_config("ParticleEmitter", {
    "TOP_DESCRIPTION": "This node creates a particle emitter with the specified properties. It can be used in conjunction with particle system mask nodes to create complex particle effects. They can be chained together to add many to a given simulation.",
    "ADDITIONAL_INFO": """
- `emitter_x`: X-coordinate of the emitter (0.0 to 1.0, left to right)
- `emitter_y`: Y-coordinate of the emitter (0.0 to 1.0, up to down)
- `particle_direction`: Direction of particle emission in degrees (0.0 to 360.0, clockwise)
- `particle_spread`: Spread angle of particle emission in degrees (0.0 to 360.0, clockwise)
- `particle_size`: Size of emitted particles (1.0 to 400.0)
- `particle_speed`: Speed of emitted particles (1.0 to 1000.0)
- `emission_rate`: Rate of particle emission (0.1 to 100.0)
- `color`: Color of emitted particles (RGB string)
- `initial_plume`: Initial burst of particles (0.0 to 1.0)
- `start_frame`: Frame to start the emission (0 to 10000)
- `end_frame`: Frame to end the emission (0 to 10000)

Optional inputs:
- `emitter_movement`: Movement settings for the emitter (EMITTER_MOVEMENT type)
- `spring_joint_setting`: Spring joint configuration for particles (SPRING_JOINT_SETTING type)
- `particle_modulation`: Modulation settings for particle properties over time (PARTICLE_MODULATION type)
"""
})

add_node_config("MovingShape", {
    "TOP_DESCRIPTION": "Generate animated mask sequences featuring a moving shape with customizable parameters.",
    "ADDITIONAL_INFO": """
- `frame_width`: Width of each frame (1-3840 pixels)
- `frame_height`: Height of each frame (1-2160 pixels)
- `num_frames`: Number of frames in the sequence (1-120)
- `rgb`: Color of the shape in RGB format, e.g., "(255,255,255)"
- `shape`: Shape type ("square", "circle", or "triangle")
- `shape_width_percent`: Width of the shape as a percentage of frame width (0-100%)
- `shape_height_percent`: Height of the shape as a percentage of frame height (0-100%)
- `shape_start_position_x`: Starting X position of the shape (-100 to 100)
- `shape_start_position_y`: Starting Y position of the shape (-100 to 100)
- `shape_end_position_x`: Ending X position of the shape (-100 to 100)
- `shape_end_position_y`: Ending Y position of the shape (-100 to 100)
- `movement_type`: Type of movement ("linear", "ease_in_out", "bounce", or "elastic")
- `grow`: Growth factor of the shape during animation (0-100)
- `palindrome`: Whether to reverse the animation sequence (True/False)
- `delay`: Number of static frames at the start (0-60)

This node creates a mask sequence with a moving shape, allowing for various animations and transformations.
"""
})

add_node_config("TextMaskNode", {
    "TOP_DESCRIPTION": "Generate mask and image sequences featuring customizable text.",
    "ADDITIONAL_INFO": """
- `width`: Width of the output image (1-8192 pixels)
- `height`: Height of the output image (1-8192 pixels)
- `text`: The text to be rendered
- `font`: Font to be used (selectable from system fonts)
- `font_size`: Size of the font (1-1000)
- `font_color`: Color of the text in RGB format, e.g., "(255,255,255)"
- `background_color`: Color of the background in RGB format, e.g., "(0,0,0)"
- `x_position`: Horizontal position of the text (0.0-1.0, where 0.5 is center)
- `y_position`: Vertical position of the text (0.0-1.0, where 0.5 is center)
- `rotation`: Rotation angle of the text (0-360 degrees)
- `max_width_ratio`: Maximum width of text as a ratio of image width (0.1-1.0)
- `batch_size`: Number of images to generate in the batch (1-10000)
"""
})

add_node_config("_mfc", {
    "TOP_DESCRIPTION": "Basic mask from color.",
    "ADDITIONAL_INFO": """
This is an abstract base class that provides common functionality for mask function components.
It is not meant to be used directly but serves as a foundation for other mask-related nodes.

Key features:
- Implements common methods for mask operations
- Provides a structure for derived classes to follow
- Ensures consistency across different mask function components
"""
})

add_node_config("DownloadOpenUnmixModel", {
    "TOP_DESCRIPTION": "Downloads and loads Open Unmix models for audio classification",
    "ADDITIONAL_INFO": """
-umxl (default) trained on private stems dataset of compressed stems. Note, that the weights are only licensed for non-commercial use (CC BY-NC-SA 4.0).

-umxhq trained on MUSDB18-HQ which comprises the same tracks as in MUSDB18 but un-compressed which yield in a full bandwidth of 22050 Hz.


"""
})

add_node_config("FeatureMixer", {
    "TOP_DESCRIPTION": "Advanced feature modulation node for fine-tuning and shaping feature values.",
    "ADDITIONAL_INFO": """
- `feature`: Input feature to be processed (FEATURE type)
- `base_gain`: Overall amplification of the feature values (0.0 to 10.0). Higher values increase the overall intensity.
- `floor`: Minimum value for the processed feature (0.0 to 1.0). Prevents values from going below this threshold.
- `ceiling`: Maximum value for the processed feature (0.0 to 10.0). Caps values at this upper limit.
- `peak_sharpness`: Sharpness of peaks in the feature curve (0.1 to 10.0). Higher values create more pronounced peaks.
- `valley_sharpness`: Sharpness of valleys in the feature curve (0.1 to 10.0). Higher values create deeper valleys.
- `attack`: Speed at which the envelope follower responds to increasing values (0.01 to 1.0). Lower values create slower attack.
- `release`: Speed at which the envelope follower responds to decreasing values (0.01 to 1.0). Lower values create slower release.
- `smoothing`: Amount of smoothing applied to the final curve (0.0 to 1.0). Higher values create smoother transitions.

This node provides extensive control over feature modulation, allowing for complex shaping of feature values over time. It combines multiple processing stages including gain, waveshaping, envelope following, and smoothing to create highly customized feature curves for mask modulation.

Outputs:
- Processed FEATURE
- Visualization of the processed feature (IMAGE type)
"""
})

add_node_config("FeatureToWeightsStrategy", {
    "TOP_DESCRIPTION": "Converts a FEATURE input into a WEIGHTS_STRATEGY for use with IPAdapter nodes.",
    "ADDITIONAL_INFO": """
- `feature`: Input feature to be converted (FEATURE type)

This node takes a FEATURE input and converts it into a WEIGHTS_STRATEGY that can be used with IPAdapter nodes. It creates a custom weights strategy based on the feature values for each frame.
This node is particularly useful for creating dynamic, feature-driven animations with IPAdapter, where the strength of the adaptation can vary over time based on extracted features from audio, video, or other sources.

"""
})

NODE_CONFIGS["FlexImageBase"] = {
    "BASE_DESCRIPTION": """

## Common Parameters
- `images`: Input image sequence (IMAGE type)
- `feature`: Feature used to modulate the effect (FEATURE type)
- `feature_pipe`: Feature pipe containing frame information (FEATURE_PIPE type)
- `strength`: Overall strength of the effect (0.0 to 1.0)
- `feature_threshold`: Minimum feature value to apply the effect (0.0 to 1.0)
- `modulate_param`: Parameter to be modulated by the feature
- `modulation_mode`: How the feature modulates the parameter ("relative" or "absolute")
"""
}

add_node_config("FlexImagePosterize", {
    "TOP_DESCRIPTION": "Applies a posterization effect to the image, reducing the number of colors.",
    "ADDITIONAL_INFO": """
- `max_levels`: Maximum number of color levels per channel (2 to 256)
- `dither_strength`: Intensity of dithering effect (0.0 to 1.0)
- `channel_separation`: Degree of separation between color channels (0.0 to 1.0)
- `gamma`: Gamma correction applied before posterization (0.1 to 2.2)
"""
})

add_node_config("FlexImageKaleidoscope", {
    "TOP_DESCRIPTION": "Creates a kaleidoscope effect by mirroring and rotating segments of the image.",
    "ADDITIONAL_INFO": """
- `segments`: Number of mirror segments (2 to 32)
- `center_x`: X-coordinate of the effect center (0.0 to 1.0)
- `center_y`: Y-coordinate of the effect center (0.0 to 1.0)
- `zoom`: Zoom factor for the effect (0.1 to 2.0)
- `rotation`: Rotation angle of the effect (0.0 to 360.0 degrees)
- `precession`: Rate of rotation change over time (-1.0 to 1.0)
- `speed`: Speed of the effect animation (0.1 to 5.0)
"""
})

add_node_config("FlexImageColorGrade", {
    "TOP_DESCRIPTION": "Applies color grading to the image using a Look-Up Table (LUT).",
    "ADDITIONAL_INFO": """
- `intensity`: Strength of the color grading effect (0.0 to 1.0)
- `mix`: Blend factor between original and graded image (0.0 to 1.0)
- `lut_file`: Path to the LUT file (optional)
"""
})

add_node_config("FlexImageGlitch", {
    "TOP_DESCRIPTION": "Creates a glitch effect by applying horizontal shifts and color channel separation.",
    "ADDITIONAL_INFO": """
- `shift_amount`: Magnitude of horizontal shift (0.0 to 1.0)
- `scan_lines`: Number of scan lines to add (0 to 100)
- `color_shift`: Amount of color channel separation (0.0 to 1.0)
"""
})

add_node_config("FlexImageChromaticAberration", {
    "TOP_DESCRIPTION": "Simulates chromatic aberration by shifting color channels.",
    "ADDITIONAL_INFO": """
- `shift_amount`: Magnitude of color channel shift (0.0 to 0.1)
- `angle`: Angle of the shift effect (0.0 to 360.0 degrees)
"""
})

add_node_config("FlexImagePixelate", {
    "TOP_DESCRIPTION": "Applies a pixelation effect to the image.",
    "ADDITIONAL_INFO": """
- `pixel_size`: Size of each pixelated block (1 to 100 pixels)
"""
})

add_node_config("FlexImageBloom", {
    "TOP_DESCRIPTION": "Adds a bloom effect to bright areas of the image.",
    "ADDITIONAL_INFO": """
- `threshold`: Brightness threshold for the bloom effect (0.0 to 1.0)
- `blur_amount`: Amount of blur applied to the bloom (0.0 to 50.0)
- `intensity`: Strength of the bloom effect (0.0 to 1.0)
"""
})

add_node_config("FlexImageTiltShift", {
    "TOP_DESCRIPTION": "Creates a tilt-shift effect, simulating a shallow depth of field.",
    "ADDITIONAL_INFO": """
- `blur_amount`: Strength of the blur effect (0.0 to 50.0)
- `focus_position_x`: X-coordinate of the focus center (0.0 to 1.0)
- `focus_position_y`: Y-coordinate of the focus center (0.0 to 1.0)
- `focus_width`: Width of the focus area (0.0 to 1.0)
- `focus_height`: Height of the focus area (0.0 to 1.0)
- `focus_shape`: Shape of the focus area ("rectangle" or "ellipse")
"""
})