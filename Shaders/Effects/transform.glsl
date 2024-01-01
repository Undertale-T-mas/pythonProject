#version 330 core

in vec2 fragTexCoord;
uniform sampler2D sampler;

uniform float iScale;
uniform float iRotate;
uniform float iBrimFade;
uniform float iAlpha;
uniform vec2 iCentreUV;
uniform vec2 iOffset;

out vec4 fragColor;

void main()
{
    // do rgb split
    vec2 texCoord = fragTexCoord;
    float len = length(texCoord - iCentreUV);
    float dir = atan((texCoord - iCentreUV).y, (texCoord - iCentreUV).x);
    dir += iRotate;
    len *= iScale;
    vec2 pos = iCentreUV + iOffset + vec2(cos(dir) * len, sin(dir) * len);
    vec4 col = texture(sampler, pos);
    float dist = length((texCoord - vec2(0.5, 0.5)) * vec2(1, 0.5));
    dist = max(dist - 0.6 + iBrimFade, 0.0);

    col.r *= iAlpha; col.g *= iAlpha; col.b *= iAlpha;
    col.r -= dist; col.g -= dist, col.b -= dist;
    fragColor = col;
}