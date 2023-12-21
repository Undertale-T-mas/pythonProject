#version 330 core

in vec2 fragTexCoord;
uniform sampler2D sampler;
uniform sampler2D sampler_old;

uniform float scale;

out vec4 fragColor;

void main()
{
    vec2 texCoord = fragTexCoord;
    fragColor = vec4(mix(texture(sampler_old, texCoord), texture(sampler, texCoord), scale).xyz, 1.0);
}