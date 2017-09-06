varying vec3 normal;
varying vec3 P;//position vec
varying vec3 N;//normal vec

void main() {
	normal = gl_NormalMatrix * gl_Normal + 1;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

	P = vec3(gl_ModelViewMatrix * gl_Vertex);
    N = normalize(gl_NormalMatrix * gl_Normal).xyz;
    gl_TexCoord[0] = gl_MultiTexCoord0;
}