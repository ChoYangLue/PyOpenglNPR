varying vec3 normal;
uniform sampler2D sampler;
varying vec3 P;//position vec

const float redScale   = 0.298912;
const float greenScale = 0.586611;
const float blueScale  = 0.114478;
const vec3  monochromeScale = vec3(redScale, greenScale, blueScale);

uniform float shadetype;
uniform float lineScale;
uniform float dotScale;

void main() {
    float intensity;
    vec4 color;
    vec3 n = normalize(normal);
    vec3 l = normalize(gl_LightSource[0].position).xyz;

	//texture color
	vec4 texColor = texture2D(sampler, gl_TexCoord[0].st);
	float grayColor = dot(texColor.rgb, monochromeScale);
    texColor = vec4(vec3(grayColor), 1.0);

	//float lineScale;
	//lineScale = 1.2;

	vec2 v = gl_FragCoord.xy * lineScale;
	float f = sin(v.x + v.y);
	if (shadetype < 0.5){
		v = gl_FragCoord.xy * dotScale;
		f = (sin(v.x) * 0.5 + 0.5) + (sin(v.y) * 0.5 + 0.5);
	} else {
		v = gl_FragCoord.xy * lineScale;
		f = sin(v.x + v.y);
	}

    // quantize to 5 steps (0, .25, .5, .75 and 1)
    intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;

	color =  vec4(intensity,intensity,intensity,1.0);
	if(intensity>=0.75){
		intensity = 0.5;
		color =  vec4(intensity,intensity,intensity,1.0);
		//color =  vec4(f,f,f,1.0);
	}
	else {
		intensity = 0.0;
		//color =  vec4(intensity,intensity,intensity,0.0);
		color =  vec4(f,f,f,1.0);
	}

/*
	vec3 eyeV = normalize(-P.xyz);        //eyevec
	if (dot(eyeV, n) <= 0.05 && dot(eyeV, n) >= -0.05){
		color = vec4(1.0, 0.6, 0.0, 1.0);
	}
*/
    //gl_FragColor = color;
	gl_FragColor = texColor + color;
}