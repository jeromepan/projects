#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
// [einirv]- commented out (no malloc.h in OS X)
//#include <malloc.h>
#include "cquadpak.h"
#include "dqdefs.h"

double dqawo(double f(double),double a,double b,double omega, int sincos,
	double epsabs,double epsrel,double *abserr,int *neval,
	int *ier)
{
    double **chebmo,result;
    int i,momcom;

	if ((chebmo = (double **)calloc(MAXP1,sizeof(double *))) == NULL) {
		fprintf(stderr,"Out of memory in DQAWO!\n");
		exit(1);
	}
	for (i = 0;i < MAXP1; i++) {
		if ((chebmo[i] = (double *)calloc(25,sizeof(double))) == NULL) {
			fprintf(stderr,"Out of memory in DQAWO!\n");
			exit(1);
		}
	}

	momcom = 0;
	result = dqfour(f,a,b,omega,sincos,epsabs,epsrel,
        1,MAXP1,abserr,neval,ier,&momcom,chebmo);
	for (i = 0;i < MAXP1; i++)
		free(chebmo[i]);
	free(chebmo);
	return result;
}
