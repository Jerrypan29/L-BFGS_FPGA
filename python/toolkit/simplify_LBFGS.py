from toolkit.doublefloat import quant_nd
import numpy as np
from  toolkit.approx_derivative import  *
import toolkit.simplify_linesearch as simplify
import toolkit.simplify_linesearch_f as simplify_f
from toolkit.quant import Quantizer
import time
import pandas as pd
import os
def print_into_file(out_file,out_var):
    if not os.path.exists(out_file):
        with open(out_file,"w") as filename:
            print("create file\n")

    with open(out_file,"a") as filename:
        out_var = out_var.flatten()
        for item in out_var:
            filename.write(str(item))
            filename.write('\n')
def InvHessProduct(gxk,s,y,rho,m):
    #gxk = gxk.astype(np.single)

    q = np.array(gxk, copy=True)
    #q = q.astype(np.single)
    if q.ndim == 2 and q.shape[1] == 1: 
        q = q.reshape(-1)
    maxcor=min(m,s.shape[0])
    alpha = np.empty(maxcor)

    for i in range(maxcor - 1, -1, -1):
        #print("test",np.dot(s[i], q))
        alpha[i] = rho[i] * np.dot(s[i], q)
        q = q - alpha[i] * y[i]
    
    r = q
    for i in range(maxcor):
        beta = rho[i] * np.dot(y[i], r)
        r = r + s[i] * (alpha[i] - beta)
    return r

max_fp16 = np.finfo(np.float16).max
def del_inf(arr):
    arr[arr == np.inf] = max_fp16
    arr[arr == -np.inf] = -max_fp16
def InvHessProduct_f16(gxk,s,y,rho,m):
    
    #Quant_ = Quantizer()
    #Qua = Quant_.Qua
    gxk = gxk.astype(np.float16)
    del_inf(gxk)
    s = s.astype(np.float16)
    del_inf(s)
    y = y.astype(np.float16)
    del_inf(y)
    rho = rho.astype(np.float16)
    del_inf(rho)
    #m = m.astype(np.single)

    q = np.array(gxk, copy=True)
    #print(q)
    #q = q.astype(np.float16)
    #del_inf(q)
    #print("ha",q.dtype)
    print_into_file("bfgs/s.txt",s)
    print_into_file("bfgs/y.txt",y)
    print_into_file("bfgs/q.txt",q)
    if q.ndim == 2 and q.shape[1] == 1: #���������????��???
        q = q.reshape(-1)
    maxcor=min(m,s.shape[0])
    alpha = np.empty(maxcor)

    #print("hahaha",m,maxcor,alpha)
    
    for i in range(maxcor - 1, -1, -1):
        #print("i="+str(i))
        #print("maxcor"+str(maxcor))
        #print(rho,s,q)
        alpha[i] = rho[i] * np.dot(s[i], q)
        #print(alpha)
        #alpha = alpha.astype(np.float16)

        #print("ha",alpha.dtype,rho.dtype,s.dtype,q.dtype)
        #del_inf(alpha)
        q = q - alpha[i] * y[i]
        #print(q)
      
        #q = q.astype(np.float16)
        del_inf(q)
    r = q
    for i in range(maxcor):
        beta = rho[i] * np.dot(y[i], r)
        #beta = beta.astype(np.float16)
        del_inf(beta)
        r = r + s[i] * (alpha[i] - beta)
        #r = r.astype(np.float16)
        del_inf(beta)
        #print("ha",beta.dtype,r.dtype)
    return r

def InvHessProduct_f16_87(gxk,s,y,rho,m):

    gxk = quant_nd(gxk)
    s = quant_nd(s)
    y = quant_nd(y)
    rho = quant_nd(rho)

    q = np.array(gxk, copy=True)
    if q.ndim == 2 and q.shape[1] == 1: 
        q = q.reshape(-1)
    maxcor=min(m,s.shape[0])
    alpha = np.empty(maxcor)

    for i in range(maxcor - 1, -1, -1):
        alpha[i] = rho[i] * np.dot(s[i], q)
        alpha = quant_nd(alpha)
        q = q - alpha[i] * y[i]
        q = quant_nd(q)
    r = q
    for i in range(maxcor):
        beta = rho[i] * np.dot(y[i], r)
        beta = quant_nd(beta)
        r = r + s[i] * (alpha[i] - beta)
        r = quant_nd(r)
    return r


def InvHessProduct_f(gxk,s,y,rho,m):
    
    Quant_ = Quantizer()
    Qua = Quant_.Qua
    gxk = gxk.astype(np.single)
    s = s.astype(np.single)
    y = y.astype(np.single)
    rho = rho.astype(np.single)
    #m = m.astype(np.single)

    q = np.array(gxk, copy=True)
    q = q.astype(np.single)
    #print(q)
    #print("ha",q.dtype)
    #print_into_file("bfgs/s.txt",s)
    #print_into_file("bfgs/y.txt",y)
    #print_into_file("bfgs/q.txt",q)
    if q.ndim == 2 and q.shape[1] == 1: #���������????��???
        q = q.reshape(-1)
    maxcor=min(m,s.shape[0])
    alpha = np.empty(maxcor)

    for i in range(maxcor - 1, -1, -1):
        alpha[i] = rho[i] * np.dot(s[i], q)
        alpha = alpha.astype(np.single)
        q = q - alpha[i] * y[i]
        #print(type(q),q)
        q = q.astype(np.single)
    r = q
    for i in range(maxcor):
        beta = rho[i] * np.dot(y[i], r)
        beta = beta.astype(np.single)
        #print(r , s[i] * (alpha[i] - beta))
        r = r + s[i] * (alpha[i] - beta)
        r = r.astype(np.single)
        #print("ha",beta.dtype,r.dtype)
    return r

def InvHessProduct_1(gxk,s,y,rho,m):

    Quant_ = Quantizer()
    Qua = Quant_.Qua
    q = np.array(gxk, copy=True)
    print(q,q.dtype)
    #print_into_file("bfgs/s.txt",s)
    #print_into_file("bfgs/y.txt",y)
    #print_into_file("bfgs/q.txt",q)
    if q.ndim == 2 and q.shape[1] == 1: #���������????��???
        q = q.reshape(-1)
    maxcor=min(m,s.shape[0])
    alpha = np.empty(maxcor)
    #print(alpha.size,s.size,q.size)
    #print(s)
    #print(np.mean(s-Qua(s)))
    #print(s.size)
    s = Qua(s,num_bit = 32 ,decimal_bit = 25)
    y = Qua(y,num_bit = 32 ,decimal_bit = 12)
    q = Qua(q,num_bit = 34 ,decimal_bit = 14)
    rho = Qua(rho,num_bit = 34 ,decimal_bit = 14)
    #print(rho,'qua')
    for i in range(maxcor - 1, -1, -1):
        alpha[i] = rho[i] * np.dot(s[i], q)
        #alpha[i] = Qua(alpha[i],num_bit = 32 ,decimal_bit = 14)
        alpha[i] = Quant_.quant(alpha[i],num_bit = 32 ,decimal_bit = 14)
        #print_into_file("bfgs/alpha.txt",alpha)
        q = q - alpha[i] * y[i]
        q = Qua(q,num_bit = 32 ,decimal_bit = 14)
        #print_into_file("bfgs/q.txt",q)
    r = q
    for i in range(maxcor):
        beta = rho[i] * np.dot(y[i], r)
        #print(beta)
        beta = Qua(beta,num_bit = 40 ,decimal_bit = 12)
        #print(beta,'qua')
        #print_into_file("bfgs/beta.txt",beta)
        r = r + s[i] * (alpha[i] - beta)
        r = Qua(r,num_bit = 32 ,decimal_bit = 14)
        #print_into_file("bfgs/r.txt",r)
    return r


def _check_ftol(fx,fx_next,ftol=1e-5):
    temp=max(abs(fx), abs(fx_next))
    temp=max(temp,1.0)
    if (fx-fx_next)/temp<=ftol:
        #print("-----satisfy the ftol-----")
        return True
    else:
        return False
def _check_gtol(g,gtol=1e-5):
    for i in range (g.shape[0]):
        if abs(g[i])>gtol:
            return False
    #print("\n-----satisfy the gtol-----\n")
    return True

def fmin_l_bfgs_f(fun,x0,prime=None,args=(), maxcor=10, ftol=2.2204460492503131e-09,gtol= 1e-5,maxiter=15000,maxls=20,out_file_name='./test_out/test_csv.csv'):
    '''

    :param func:
    :param x0:
    :param fprime:
    :param args:
    :param mxcor:
    :param ftol:
    :param gtol:
    :param maxiter:
    :param maxls:  Maximum number of line search steps (per iteration). Default is 20
    :return:
    '''
    ftol = quant_nd(ftol)
    gtol - quant_nd(gtol)
    def func(x):
        return fun(x,*args)


    def fprime(x):
        if prime is None :
            return approx_derivative(fun,x,args=args)
        return prime(x,*args)
    total=0
    cnt_iter=1
    fx0=func(x0)
    g0=fprime(x0)

    search_direction0=-g0
    fx_last = fx0 + np.linalg.norm(g0) / 2

    start=time.time()
    alpha0=simplify_f.line_search_BFGS(func,x0,search_direction0,g0,fx0)[0]
    end=time.time()
    total+=end-start
    delta0 = alpha0*search_direction0
    x1=x0+delta0  
    fx1=func(x1)
    #print("fx:{}".format(fx1))
    if _check_ftol(fx0,fx1,ftol):
        return x1,fx1
    
    g1=fprime(x1)
    
    if _check_gtol(g1,gtol):
        return x1,fx1

    s0=x1-x0
    y0=g1-g0
    rho0=np.empty(1)
    s0 = quant_nd(s0)
    y0 = quant_nd(y0)

    rho0[0]=1.0/np.dot(s0,y0)
    rho0 = quant_nd(rho0)
    
    s=s0.copy()
    y=y0.copy()
    rho=rho0.copy()
    s=s.reshape(-1,s.shape[0])
    y=y.reshape(-1,y.shape[0])
    rho=rho.reshape(-1,1)
    x_current=x1.copy()
    fx_current=fx1
    gx_current=g1.copy()

    df = pd.DataFrame()
    item = pd.Series({'index':0,'alpha':alpha0,'rho':rho0[0], 'x0':x0, 'x1-x0':s0, 'g1-g0':y0})
    df = df.append(item,ignore_index = True)
    #print('******************\n',df)
    #count = 1
    while(True):
        r=InvHessProduct(gx_current,s,y,rho,maxcor)
        search_direction_current=-r
        start=time.time()
        alpha_current=simplify_f.line_search_BFGS(func,x_current,search_direction_current,gx_current,fx_current)[0]
        end = time.time()
        total+=end-start
        
        x_next=x_current+alpha_current*search_direction_current
        
        fx_next=func(x_next)
        # print("fx:{}".format(fx_next))
        if _check_ftol(fx_current,fx_next,ftol):
            '''
            file = open('./test_out/res.txt','r+')
            file.read()
            file.write('time of linesearch:')
            file.write(str(total))
            file.write('\n')
            file.close()
            '''
            #print(out_file_name)
            df.to_csv(out_file_name, mode='a')
            return x_next,fx_next
        gx_next=fprime(x_next)
        if _check_gtol(gx_next,gtol):
            '''
            file = open('./test_out/res.txt','r+')
            file.read()
            file.write('time of linesearch:')
            file.write(str(total))
            file.write('\n')
            file.close()
            '''
            df.to_csv(out_file_name, mode='a')
            return x_next,fx_next
        
        s_new=x_next-x_current
        y_new=gx_next-gx_current

        s_new = quant_nd(s_new)
        y_new = quant_nd(y_new)

        rho_new=1.0/np.dot(s_new,y_new)

        rho_new = quant_nd(rho_new)

        if(s.shape[0]>=maxcor):
            s=np.delete(s,0,0)
            y=np.delete(y,0,0)
            rho=np.delete(rho,0,0)
        s_temp = np.append(s, s_new)
        s = s_temp.reshape(-1, s.shape[1])
        y_temp = np.append(y, y_new)
        y = y_temp.reshape(-1, y.shape[1])
        rho_temp = np.append(rho, rho_new)
        rho = rho_temp.reshape(-1, 1)

        x_current=x_next
        fx_current=fx_next
        gx_current=gx_next
        if cnt_iter>=maxiter:
            print("amout to maxiter")
            break

        item = pd.Series({'index':cnt_iter,'alpha':alpha_current,'rho':rho_new, 'x0':x_current, 'x1-x0':s_new, 'g1-g0':y_new})

        df = df.append(item,ignore_index = True)
        
        cnt_iter=cnt_iter+1

    df.to_csv(out_file_name, mode='a')
    return x_current,func(x_current)



def fmin_l_bfgs(fun,x0,prime=None,args=(), maxcor=10, ftol=1e-5,gtol= 1e-5,maxiter=15000,maxls=20,out_file_name='./test_out/test_csv.csv'):
    
    '''

    :param func:
    :param x0:
    :param fprime:
    :param args:
    :param mxcor:
    :param ftol:
    :param gtol:
    :param maxiter:
    :param maxls:  Maximum number of line search steps (per iteration). Default is 20
    :return:
    '''
    def func(x):
        return fun(x,*args)


    def fprime(x):
        if prime is None :
            
            return approx_derivative(fun,x,args=args,abs_step=3.07598093058913946151733398438E-4)
        return prime(x,*args)
    total=0
    cnt_iter=1
    start=time.time()
    start_loop=time.time()
    fx0=func(x0)
    end_loop=time.time()
    print("round 0")
    print("object function value:",fx0)
    print("iteration time:",end_loop-start_loop)
    print("total time:",end_loop-start)
    print("round 1")
    start_loop=time.time()

    grand_start=time.time()
    g0=fprime(x0)
    grand_end=time.time()
    print("GCU time:",grand_end-grand_start)
    search_direction0=-g0
    start_slu=time.time()
    alpha0=simplify.line_search_BFGS(func,x0,search_direction0,g0,fx0)[0]
    end_slu=time.time()
    print("LSU time:",end_slu-start_slu)
  
    delta0 = alpha0*search_direction0
    x1=x0+delta0
    
    fx1=func(x1)
    print("alpha:",alpha0)
    print("object function value:",fx1)

    if _check_ftol(fx0,fx1,ftol):
        
        end=time.time()
        total=end-start
        print("iteration time:",end-start_loop)
        print("total time:",total)
        return x1,fx1
    
    g1=fprime(x1)
    
    if _check_gtol(g1,gtol):
        end=time.time()
        total=end-start
        print("iteration time:",end-start_loop)
        print("total time:",total)
        return x1,fx1
    end_loop=time.time()
    print("iteration time:",end_loop-start_loop)
    print("total time:",end_loop-start)
    print("round 2")

    start_loop=time.time()
    s0=x1-x0
    y0=g1-g0
    rho0=np.empty(1)
    rho0[0]=1.0/np.dot(s0,y0)
    
    s=s0.copy()
    y=y0.copy()
    rho=rho0.copy()
    s=s.reshape(-1,s.shape[0])
    y=y.reshape(-1,y.shape[0])
    rho=rho.reshape(-1,1)
    x_current=x1.copy()
    fx_current=fx1
    gx_current=g1.copy()

    df = pd.DataFrame()
    item = pd.Series({'index':0,'alpha':alpha0,'rho':rho0[0], 'x0':x0, 'x1-x0':s0, 'g1-g0':y0})

    df = pd.concat([df, item], ignore_index=True)
    round=3
    while(True):
        start_sdu=time.time()
        r=InvHessProduct(gx_current,s,y,rho,maxcor)  #maxcor=10
        end_sdu=time.time()
        print("SDU time:",end_sdu-start_sdu)

        search_direction_current=-r
        start_slu=time.time()
        alpha_current=simplify.line_search_BFGS(func,x_current,search_direction_current,gx_current,fx_current)[0]
        end_slu=time.time()
        print("LSU time:",end_slu-start_slu)
        x_next=x_current+alpha_current*search_direction_current  
        fx_next=func(x_next)
        print("alpha:",alpha_current)
        print("object function value:",fx_next)

        if _check_ftol(fx_current,fx_next,ftol):
            df.to_csv(out_file_name, mode='a')
            end=time.time()
            total=end-start
            print("iteration time:",end-start_loop)
            print("total time:",total)
            return x_next,fx_next
        gx_next=fprime(x_next)
        if _check_gtol(gx_next,gtol):
            df.to_csv(out_file_name, mode='a')
            end=time.time()
            total=end-start
            print("iteration time:",end-start_loop)
            print("total time:",total)
            return x_next,fx_next
        end_loop=time.time()
        print("iteration time:",end_loop-start_loop)
        print("total time:",end_loop-start)
        print("round {}".format(round))
        round=round+1
        start_loop=time.time()
        s_new=x_next-x_current
        y_new=gx_next-gx_current
        rho_new=1.0/np.dot(s_new,y_new)
        if(s.shape[0]>=maxcor):
            s=np.delete(s,0,0)
            y=np.delete(y,0,0)
            rho=np.delete(rho,0,0)
        s_temp = np.append(s, s_new)
        s = s_temp.reshape(-1, s.shape[1])
        y_temp = np.append(y, y_new)
        y = y_temp.reshape(-1, y.shape[1])
        rho_temp = np.append(rho, rho_new)
        rho = rho_temp.reshape(-1, 1)

        x_current=x_next
        fx_current=fx_next
        gx_current=gx_next
        if cnt_iter>=maxiter:
            print("amout to maxiter")
            break

        item = pd.Series({'index':cnt_iter,'alpha':alpha_current,'rho':rho_new, 'x0':x_current, 'x1-x0':s_new, 'g1-g0':y_new})
        
        #print('#################',x_current.shape)
        df = df._append(item,ignore_index = True)
        
        cnt_iter=cnt_iter+1
        #print(df.shape[0])
    end_loop=time.time()
    
    print("iteration time:",end_loop-start_loop)
    end=time.time()
    total=end-start
    print("total time:",total)
    df.to_csv(out_file_name, mode='a')
    return x_current,func(x_current)

