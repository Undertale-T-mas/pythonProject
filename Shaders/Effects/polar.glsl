#version 330 core

in vec2 fragTexCoord;
uniform vec2 screen_size;
uniform vec2 iCentre;
uniform sampler2D sampler;

uniform float iIntensity;

out vec4 fragColor;
const float pi = 3.1415926535;

void main()
{
    vec2 source = fragTexCoord;
    float dir = atan(fragTexCoord.y - iCentre.y, fragTexCoord.x - iCentre.x);
    float len = fract(length(fragTexCoord - iCentre / screen_size) * 2.0);
    vec2 destin = vec2(dir / pi + 0.5, len);
    vec2 final = mix(source, destin, iIntensity);
    fragColor = texture(sampler, final);
}