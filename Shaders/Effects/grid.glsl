#version 330 core

in vec2 fragTexCoord;

uniform vec2 screen_size;
uniform float iTime;
uniform sampler2D sampler;
uniform sampler2D noise;

const float pixSizeX = 5.0;
const float pixSizeY = 5.0;

uniform vec3 iBlendColor = vec3(0.7, 0.53, 0.9);
uniform float iDotSize = 0.39;

out vec4 fragColor;

vec2 mnoise2(float x, float y){
    return texture(noise, vec2(x, y)).rg;
}

void main()
{
    float indexX = fragTexCoord.x * screen_size.x - 0.5;
    float indexY = fragTexCoord.y * screen_size.y - 0.5;
    float cellX = floor(indexX / pixSizeX) * pixSizeX;
    float cellY = floor(indexY / pixSizeY) * pixSizeY;

    float texAvg = 0.0;

    vec2 currUV = vec2(cellX / screen_size.x, cellY / screen_size.y);
    vec3 currTexVal = texture(sampler, currUV).rgb;
    texAvg += 0.2 * (0.3 * currTexVal.r + 0.59 * currTexVal.g + 0.11 * currTexVal.b);

    currTexVal = texture(sampler, currUV - vec2(1.5 / screen_size.x, 0.0)).rgb;
    texAvg += 0.2 * (0.3 * currTexVal.r + 0.59 * currTexVal.g + 0.11 * currTexVal.b);

    currTexVal = texture(sampler, currUV + vec2(1.5 / screen_size.x, 0.0)).rgb;
    texAvg += 0.2 * (0.3 * currTexVal.r + 0.59 * currTexVal.g + 0.11 * currTexVal.b);

    currTexVal = texture(sampler, currUV - vec2(0.0, 1 / screen_size.y)).rgb;
    texAvg += 0.2 * (0.3 * currTexVal.r + 0.59 * currTexVal.g + 0.11 * currTexVal.b);

    currTexVal = texture(sampler, currUV + vec2(0.0, 1 / screen_size.y)).rgb;
    texAvg += 0.2 * (0.3 * currTexVal.r + 0.59 * currTexVal.g + 0.11 * currTexVal.b);

    /*vec2 uv = currUV;
    vec2 flame_col = mnoise2(uv + mnoise2(1.5 * uv + mnoise2(2.0 * uv, -0.8 * iTime), -0.52 * iTime), -0.4 * iTime) - 0.75;

    flame_col.g = min(0.5 * flame_col.g, flame_col.r);
    flame_col *= smoothstep(-0.25, -0.5, uv.y - 0.2 + flame_col.r - 1.0 * min(1.0, uv.x * uv.x));
*/
    vec2 flame_col = vec2(0, 0);
    vec3 col = iBlendColor * texAvg;

    vec2 uvDots = vec2(fract(indexX / pixSizeX), fract(indexY / pixSizeY));
    float circle = 1.0 - step(iDotSize, length(uvDots - 0.5));
    col = col * circle;

    float f = 0.0;
    if(length(col) > 0.0)
        f = max(-0.5, sin(fragTexCoord.y * 8 - iTime * 4.0) * 0.05);

    fragColor = vec4(col + f + vec3(flame_col.y, 0.0, flame_col.x) * flame_col.x, 1.0);
}