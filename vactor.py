import numpy as np


#remember has to be in the form of a numpy array
def vct_sub(a,b):
	val=b-a
	return val
#remember has to be in the form of a numpy array
def cross_vct(a,b):
	res = np.cross(a, b)
	magnitude = res[0]**2 + res[1]**2 + res[2]**2
	return res,magnitude
	
def  distance_between_skew_lines(var1,var2,var3,var4,var5,var6,var7,var8):
	v1 = np.array([var1,var2,0])
	v2 = np.array([var3,var4,0])
	v3 = np.array([var5,var6,0])
	v4 = np.array([var7,var8,0])
	sub_res1 = vct_sub(v1,v2)
	print(sub_res1)
	sub_res2 = vct_sub(v3,v4)
	print(sub_res2)
	crs_product,magnitude = cross_vct(sub_res1,sub_res2)
	print(crs_product)
	a = sub_res1[0]
	b = sub_res2[0]
	c = crs_product[0]
	d = sub_res1[1]
	e = sub_res2[1]
	f = crs_product[1]
	g = sub_res1[2]
	h = sub_res2[2]
	i = crs_product[2]
	
	a = np.array([[a,-b,-c],[d,-e,-f],[g,-h,-i]])
	b = np.array([(var5-var1),(var6-var2),(-0 + 0)])
	coeff_array = np.linalg.solve(a,b)
	#d_1  = k(magnitude)
	return coeff_array,magnitude
	
x = np.array([-3,-4,1]) 
y = np.array([1,-2,-2])

res = vct_sub(x,y)
res1,x = distance_between_skew_lines(14,565,26,324,242,54671,244,524)
print(res1,x)                                                         
