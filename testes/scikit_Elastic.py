import sys
sys.path.append("../")
import cria_dados
import sklearn.linear_model as lm
import numpy as np
import pdb
import scipy.io
import iteracoes as it
import scipy.sparse as sparse
import pickle
f="../../le_ficheiro/someta"

dictionary, total, y =cria_dados.read_output(f+"train.txt")
X,Y=cria_dados.criaXY(dictionary,total,y,False)
media_final=0
#lamb=[(10**x)*X.shape[0] for x in xrange(-5,6)]
lamb=[1000*X.shape[0]]
#alphas=[x/10 for x in xrange(0,10)]
alphas=[1]
for lambd in lamb:
    for alphaa in alphas:
        #scipy.io.savemat("X.mat",mdict={'X':X})
        #scipy.io.savemat("Y.mat",mdict={'Y':Y})
        clf=lm.ElasticNet(l1_ratio=alphaa,alpha=lambd/X.shape[0],max_iter=10000,fit_intercept=False,normalize=False)
        cena=clf.fit(X.todense(),Y.todense())
        dictionary,temp,y=cria_dados.read_output(f+"test.txt")
        Xteste,Yteste=cria_dados.criaXY(dictionary,total,y,False)

        YP=cena.predict(Xteste)
        YP=sparse.csr_matrix(YP)
        YP=YP.transpose()
        erro=np.abs(YP-Yteste)
        media=sum(np.array(erro.todense()))/erro.shape[0]
        #print "_____________________________________"
        #print media
        #print"______________________________________"
        if media_final>media or media_final==0:
            alphaa_final=alphaa
            media_final=media
            lambd_final=lambd
print"----------------------"
print"----------------------"
print "ALPHA:",alphaa_final
print "LAMBDA:",lambd_final
print "ERRO:",media_final
#ficheiro=open("data.pkl",'wb')
#ww=cena.coef_
#ww=sparse.csr_matrix(ww).transpose()
#pickle.dump(ww,ficheiro)
#ficheiro.close()
#error=X*ww-Y
#print "OBJECTIVO:", it.get_func_lasso(error,ww,lambd)
#print ww
#print ww.shape[0]-len(np.nonzero(ww)[0])

