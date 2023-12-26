#version 330 core

in vec2 fragTexCoord;
uniform vec2 screen_size;
uniform sampler2D sampler;

uniform float iProgress;
uniform float iIntensity;
uniform float iRadius;
uniform vec2 iCentre;

out vec4 fragColor;

void main()
{
	vec2 center_vector = screen_size * fragTexCoord - iCentre;
	float vector_length = length(center_vector);
	float sus_radius = (vector_length - (iProgress * iRadius)) / 84.9294;
	float rate = iIntensity * max(0.0, 28.6983 * log(sus_radius * (5.4373 - iProgress * 5.4372)) / (sus_radius / (smoothstep(0.0001, 1.0, iProgress) * 1.5966)));
	vec2 place = fragTexCoord * screen_size + normalize(center_vector) * rate * smoothstep(1.0, 0.0, iProgress);

	fragColor = texture(sampler, place / screen_size);
	fragColor.g -= iProgress * 0.025;
}