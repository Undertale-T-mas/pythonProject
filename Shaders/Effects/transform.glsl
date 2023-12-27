#version 330 core

in vec2 fragTexCoord;
uniform sampler2D sampler;

uniform float iScale;
uniform float iRotate;
uniform float iAlpha;
uniform float iCentreUV;

out vec4 fragColor;

void main()
{
    // do rgb split
    vec2 texCoord = fragTexCoord;
    float len = length(texCoord - iCentreUV);
    float dir = atan((texCoord - iCentreUV).y, (texCoord - iCentreUV).x);
    dir += iRotate;
    len *= iScale;

}