##################################################################
import sys
sys.setrecursionlimit(10000)
##################################################################

# datatype styp =
# | STbas of strn # int, bool, ...
# | STtup of (styp, styp) # for pairs
# | STfun of (styp, styp) # for functions

class styp:
    ctag = ""
    def __str__(self):
        return ("styp(" + self.ctag + ")")
# end-of-class(styp)

# | STbas of strn # int, bool, ...
class styp_bas:
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "STbas"
    def __str__(self):
        return ("STbas(" + self.arg1 + ")")
# end-of-class(styp_bas(styp))

styp_int = styp_bas("int")
styp_bool = styp_bas("bool")

# | STtup of (styp, styp) # for pairs
class styp_tup:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "STtup"
    def __str__(self):
        return ("STtup(" + str(self.arg1) + ";" + str(self.arg2) + ")")
# end-of-class(styp_tup(styp))

styp_int2 = styp_tup(styp_int, styp_int)

# | STfun of (styp, styp) # for functions
class styp_fun:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "STfun"
    def __str__(self):
        return ("STfun(" + str(self.arg1) + ";" + str(self.arg2) + ")")
# end-of-class(styp_fun(styp))

styp_fun_int_int = styp_fun(styp_int, styp_int)

print("styp_int2 = " + str(styp_int2))
print("styp_fun_int_int = " + str(styp_fun_int_int))

def styp_equal(st1, st2):
    if (st1.ctag == "STbas"):
        return st2.ctag == "STbas" and st1.arg1 == st2.arg1
    if (st1.ctag == "STtup"):
        return st2.ctag == "STtup" \
            and styp_equal(st1.arg1, st2.arg1) and styp_equal(st1.arg2, st2.arg2)
    if (st1.ctag == "STfun"):
        return st2.ctag == "STfun" \
            and styp_equal(st1.arg1, st2.arg1) and styp_equal(st1.arg2, st2.arg2)
    raise TypeError(st1) # HX-2025-06-10: should be deadcode!

##################################################################

# datatype term =
# | TMint of int
# | TMbtf of bool
# | TMvar of strn
# | TMlam of (strn, styp, term)
# | TMapp of (term, term)
# | TMopr of (strn(*opr*), list(term))
# | TMif0 of (term, term, term)
# | TMfix of (strn(*f*), strn(*x*), styp, styp, term)

class term:
    ctag = ""
    def __str__(self):
        return ("term(" + self.ctag + ")")
# end-of-class(term)

# | TMint of int
class term_int(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMint"
    def __str__(self):
        return ("TMint(" + str(self.arg1) + ")")
# end-of-class(term_int(term))

# | TMbtf of bool
class term_btf(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMbtf"
    def __str__(self):
        return ("TMbtf(" + str(self.arg1) + ")")
# end-of-class(term_btf(term))

# | TMvar of strn
class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def __str__(self):
        return ("TMvar(" + self.arg1 + ")")
# end-of-class(term_var(term))

# | TMlam of (strn(*var*), styp, term)
class term_lam(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMlam"
    def __str__(self):
        return ("TMlam(" + self.arg1 + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")
# end-of-class(term_lam(term))

# | TMapp of (term, term)
class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def __str__(self):
        return ("TMapp(" + str(self.arg1) + ";" + str(self.arg2) + ")")
# end-of-class(term_app(term))

# | TMopr of (strn(*opr*), list(term))
class term_opr(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMopr"
    def __str__(self):
        return ("TMopr(" + self.arg1 + ";" + str(self.arg2) + ")")
# end-of-class(term_opr(term))

# | TMif0 of (term, term, term)
class term_if0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMif0"
    def __str__(self):
        return ("TMif0(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")
# end-of-class(term_if0(term))

var_x = term_var("x")

term_add = lambda a1, a2: term_opr("+", [a1, a2])
term_sub = lambda a1, a2: term_opr("-", [a1, a2])
term_mul = lambda a1, a2: term_opr("*", [a1, a2])

term_dbl = term_lam("x", styp_int, term_add(var_x, var_x))
print("term_dbl = " + str(term_dbl))

term_lt = lambda a1, a2: term_opr("<", [a1, a2])
term_lte = lambda a1, a2: term_opr("<=", [a1, a2])
term_gt = lambda a1, a2: term_opr(">", [a1, a2])
term_gte = lambda a1, a2: term_opr(">=", [a1, a2])

# TMfix of
# (strn(*f*), strn(*x*), styp(*arg*), styp(*res*), term)
class term_fix(term):
    def __init__(self, arg1, arg2, arg3, arg4, arg5):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.arg5 = arg5
        self.ctag = "TMfix"
    def __str__(self):
        return ("TMfix(" + self.arg1 + ";" + self.arg2 + ";" + str(self.arg3) + str(self.arg4) + ";" + str(self.arg5) + ")")
# end-of-class(term_fix(term))

##################################################################

# datatype tctx =
# | CXnil of ()
# | CXcons of (strn, styp, tctx)

class tctx:
    ctag = ""
    def __str__(self):
        return ("tctx(" + self.ctag + ")")
# end-of-class(tctx)

class tctx_nil(tctx):
    def __init__(self):
        self.ctag = "CXnil"
    def __str__(self):
        return ("CXnil(" + ")")
# end-of-class(tctx_nil(tctx))

class tctx_cons(tctx):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "CXcons"
    def __str__(self):
        return ("CXcons(" + self.arg1 + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")
# end-of-class(tctx_cons(tctx))

##################################################################

# #extern
# fun
# term_tpck00(tm0: term): tval
# #extern
# fun
# term_tpck01(tm0: term, ctx: tctx): tval

def term_tpck00(tm0):
    return term_tpck01(tm0, tctx_nil())

def tctx_search(ctx, x00):
    if ctx.ctag == "CXnil":
        return None
    if ctx.ctag == "CXcons":
        if ctx.arg1 == x00:
            return ctx.arg2
        else:
            return tctx_search(ctx.arg3, x00)
    raise TypeError(ctx) # HX-2025-06-10: deadcode!

def term_tpck01(tm0, ctx):
    # print("term_tpck01: tm0 = " + str(tm0))
    if (tm0.ctag == "TMint"):
        return styp_bas("int")
    if (tm0.ctag == "TMbtf"):
        return styp_bas("bool")
    if (tm0.ctag == "TMvar"):
        st0 = tctx_search(ctx, tm0.arg1)
        assert st0 is not None
        return st0
    if (tm0.ctag == "TMlam"):
        x01 = tm0.arg1
        st1 = tm0.arg2
        tmx = tm0.arg3
        ctx = tctx_cons(x01, st1, ctx)
        stx = term_tpck01(tmx, ctx)
        return styp_fun(st1, stx)
    if (tm0.ctag == "TMapp"):
        tm1 = tm0.arg1
        tm2 = tm0.arg2
        st1 = term_tpck01(tm1, ctx)
        st2 = term_tpck01(tm2, ctx)
        assert st1.ctag == "STfun"
        assert styp_equal(st1.arg1, st2)
        return st1.arg2
    if (tm0.ctag == "TMopr"):
        pnm = tm0.arg1
        ags = tm0.arg2 # list of arguments
        if (pnm == "+"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_int
        if (pnm == "-"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_int
        if (pnm == "*"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_int
        if (pnm == "-"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_int
        if (pnm == "<"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_bool
        if (pnm == ">"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_bool
        if (pnm == "="):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_bool
        if (pnm == "<="):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_bool
        if (pnm == ">="):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_bool
        if (pnm == "!="):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_bool
        if (pnm == "cmp"):
            assert len(ags) == 2
            st1 = term_tpck01(ags[0], ctx)
            st2 = term_tpck01(ags[1], ctx)
            # print("TMopr: st1 = " + str(st1))
            # print("TMopr: st2 = " + str(st2))
            assert styp_equal(st1, styp_int)
            assert styp_equal(st2, styp_int)
            return styp_int
        raise TypeError(pnm) # HX-2025-06-10: unsupported!
    if (tm0.ctag == "TMif0"):
        tm1 = tm0.arg1
        st1 = term_tpck01(tm1, ctx)
        assert styp_equal(st1, styp_bool)
        st2 = term_tpck01(tm0.arg2, ctx) # then
        st3 = term_tpck01(tm0.arg3, ctx) # else
        assert styp_equal(st2, st3)
        return st2
    # TMfix of
    # (strn(*f*), strn(*x*), styp(*arg*), styp(*res*), term)
    if (tm0.ctag == "TMfix"):
        f00 = tm0.arg1
        x01 = tm0.arg2
        st1 = tm0.arg3 # type for x01
        st2 = tm0.arg4 # type for tmx
        tmx = tm0.arg5
        stf = styp_fun(st1, st2) # type for f00
        ctx = tctx_cons(f00, stf, ctx)
        ctx = tctx_cons(x01, st1, ctx)
        stx = term_tpck01(tmx, ctx)
        assert styp_equal(st2, stx)
        return stf
    raise TypeError(tm0) # HX-2025-06-10: should be deadcode!

int_0 = term_int(0)
int_1 = term_int(1)
int_2 = term_int(2)
btf_t = term_btf(True)
btf_f = term_btf(False)
print("tpck(int_1) = " + str(term_tpck00(int_1)))
print("tpck(btf_t) = " + str(term_tpck00(btf_t)))
print("tpck(term_add(int_1, int_1)) = " + str(term_tpck00(term_add(int_1, int_1))))
print("tpck(term_lte(int_1, int_1)) = " + str(term_tpck00(term_lte(int_1, int_1))))
# HX: this one is ill-typed:
# print("tpck(term_add(int_1, btf_t)) = " + str(term_tpck00(term_add(int_1, btf_t))))
print("tpck(term_dbl) = " + str(term_tpck00(term_dbl)))

int_0 = term_int( 0 )
int_1 = term_int( 1 )
int_3 = term_int(3)
int_5 = term_int(5)
var_f = term_var("f")
var_n = term_var("n")
var_i = term_var("i")
var_r = term_var("r")
int_10 = term_int(10)
var_f2 = term_var("f2")

##################################################################

term_fact = \
  term_fix("f", "n", styp_int, styp_int, \
    term_if0(term_lte(var_n, int_0), \
      int_1, \
      term_mul(var_n, term_app(var_f, term_sub(var_n, int_1)))))

print("tpck(term_fact) = " + str(term_tpck00(term_fact)))

term_fact2 = \
  term_lam("n", styp_int, \
    term_app( \
      term_app( \
        term_fix("f", "i", styp_int, styp_fun_int_int, \
          term_lam("r", styp_int, \
            term_if0(term_gte(var_i, var_n), \
              var_r, \
              term_app( \
                term_app(var_f, term_add(var_i, int_1)), \
                term_mul(term_add(var_i, int_1), var_r))))), int_1), int_1))

print("tpck(term_fact2) = " + str(term_tpck00(term_fact2)))

##################################################################

CHNUM3 = \
  term_lam("f", styp_fun_int_int, \
    term_lam("x", styp_int, term_app(var_f, term_app(var_f, term_app(var_f, var_x)))))

print("tpck(CHNUM3) = " + str(term_tpck00(CHNUM3)))

##################################################################

# datatype treg =
# TREG of (strn(*prfx*), sint(*sffx*))

class treg:
    prfx = ""
    narg = 0
    ntmp = 100
    nfun = 100
    def __init__(self, prfx, sffx):
        self.prfx = prfx; self.sffx = sffx
    def __str__(self):
        return ("treg(" + self.prfx + str(self.sffx) + ")")
# end-of-class(treg)

def targ_new():
    treg.narg += 1
    return treg("arg", treg.narg)
def ttmp_new():
    treg.ntmp += 1
    return treg("tmp", treg.ntmp)
def tfun_new():
    treg.nfun += 1
    return treg("fun", treg.nfun)

# arg0 = targ_new()
# tmp1 = ttmp_new()
# tmp2 = ttmp_new()
# fun1 = tfun_new()
# fun2 = tfun_new()
# print("arg0 = " + str(arg0))
# print("tmp1 = " + str(tmp1))
# print("tmp2 = " + str(tmp2))
# print("fun1 = " + str(fun1))
# print("fun2 = " + str(fun2))

##################################################################

# datatype tval =
# | TVALint of sint
# | TVALbtf of bool
# | TVALchr of char
# | TVALstr of strn
# | TVALreg of treg

class tval:
    ctag = ""
    def __str__(self):
        return ("tval(" + self.ctag + ")")
# end-of-class(tval)

class tval_int(tval):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TVALint"
    def __str__(self):
        return ("TVALint(" + str(self.arg1) + ")")
# end-of-class(tval_int(tval))

class tval_btf(tval):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TVALbtf"
    def __str__(self):
        return ("TVALbtf(" + str(self.arg1) + ")")
# end-of-class(tval_btf(tval))

# datatype tins =
# | TINSmov of (treg(*dst*), tval(*src*))
# | TINSapp of (treg(*res*), treg(*fun*), treg(*arg*))
# | TINSopr of (treg(*res*), strn(*opr*), list(treg))
# | TINSfun of (treg(*f00*), treg(*x01*), tcmp(*body*))
# | TINSif0 of (treg(*res*), treg(*test*), tcmp(*then*), tcmp(*else*))

# datatype tcmp =
# | TCMP of (list(tins), treg(*res*))

class tins:
    ctag = ""
    def __str__(self):
        return ("tins(" + self.ctag + ")")
# end-of-class(tins)

class tins_mov(tins):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TINSmov"
    def __str__(self):
        return ("tins_mov(" + str(self.arg1) + ";" + str(self.arg2) + ")")

# | TINSopr of (treg(*res*), strn(*opr*), list(treg))
class tins_opr(tins):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TINSopr"
    def __str__(self):
        return ("tins_opr(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")

# | TINSapp of (treg(*res*), treg(*fun*), treg(*arg*))
class tins_app(tins):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TINSapp"
    def __str__(self):
        return ("tins_app(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")

# | TINSif0 of (treg(*res*), treg(*test*), tcmp(*then*), tcmp(*else*))
class tins_if0(tins):
    def __init__(self, arg1, arg2, arg3, arg4):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.ctag = "TINSif0"
    def __str__(self):
        return ("tins_if0(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ";" + str(self.arg4) + ")")

# | TINSfun of (treg(*f00*), tcmp(*body*))
class tins_fun(tins):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TINSfun"
    def __str__(self):
        return ("tins_fun(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ";" + ")")

# datatype tcmp =
# | TCMP of (list(tins), treg)

class tcmp:
    def __init__(self, inss, treg):
        self.arg1 = inss; self.arg2 = treg
    def __str__(self):
        return ("tcmp(" + "..." + ";" + str(self.arg2) + ")")
# end-of-class(tcmp)

##################################################################

# datatype cenv =
# | CENVnil of ()
# | CENVcons of (strn, treg, cenv)

class cenv:
    ctag = ""
    def __str__(self):
        return ("cenv(" + self.ctag + ")")
# end-of-class(cenv)

class cenv_nil(cenv):
    def __init__(self):
        self.ctag = "CENVnil"
    def __str__(self):
        return ("CENVnil(" + ")")
# end-of-class(cenv_nil(cenv))

class cenv_cons(cenv):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "CENVcons"
    def __str__(self):
        return ("CENVcons(" + self.arg1 + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")
# end-of-class(cenv_cons(cenv))

##################################################################

def term_comp00(tm0): # "computation"
    return term_comp01(tm0, cenv_nil())

def cenv_search(env, x00):
    if env.ctag == "CENVnil":
        return None
    if env.ctag == "CENVcons":
        if env.arg1 == x00:
            return env.arg2
        else:
            return cenv_search(env.arg3, x00)
    raise TypeError(env) # HX-2025-06-10: deadcode!

def term_comp01(tm0, cenv):
    if (tm0.ctag == "TMint"):
        ttmp = ttmp_new()
        ins0 = tins_mov(ttmp, tval_int(tm0.arg1))
        return tcmp([ins0], ttmp)
    if (tm0.ctag == "TMbtf"):
        ttmp = ttmp_new()
        ins0 = tins_mov(ttmp, tval_btf(tm0.arg1))
        return tcmp([ins0], ttmp)
    if (tm0.ctag == "TMvar"):
        x01 = tm0.arg1
        tmp1 = cenv_search(cenv, x01)
        return tcmp([], tmp1)
    if (tm0.ctag == "TMopr"):
        pnm = tm0.arg1
        ags = tm0.arg2 # list of arguments
        if (pnm == "+"):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, "+", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        if (pnm == "-"):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, "-", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        if (pnm == "*"):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, "*", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        if (pnm == "<"):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, "<", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        if (pnm == ">"):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, ">", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        if (pnm == "<="):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, "<=", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        if (pnm == ">="):
            assert len(ags) == 2
            cmp1 = term_comp01(ags[0], cenv)
            cmp2 = term_comp01(ags[1], cenv)
            ins1 = cmp1.arg1
            tmp1 = cmp1.arg2
            ins2 = cmp2.arg1
            tmp2 = cmp2.arg2
            ttmp = ttmp_new()
            inss = ins1 + ins2 + [tins_opr(ttmp, ">=", [tmp1, tmp2])]
            return tcmp(inss, ttmp)
        raise TypeError(pnm) # HX-2025-06-18: unsupported!
    if (tm0.ctag == "TMapp"):    
        cmp1 = term_comp01(tm0.arg1, cenv)
        cmp2 = term_comp01(tm0.arg2, cenv)
        ins1 = cmp1.arg1
        tmp1 = cmp1.arg2
        ins2 = cmp2.arg1
        tmp2 = cmp2.arg2
        ttmp = ttmp_new()
        inss = ins1 + ins2 + [tins_app(ttmp, tmp1, tmp2)]
        return tcmp(inss, ttmp)
    if (tm0.ctag == "TMif0"):
        cmp1 = term_comp01(tm0.arg1, cenv) # test
        cmp2 = term_comp01(tm0.arg2, cenv) # then
        cmp3 = term_comp01(tm0.arg3, cenv) # else
        ins1 = cmp1.arg1
        tmp1 = cmp1.arg2
        ttmp = ttmp_new()
        ins0 = tins_if0(ttmp, tmp1, cmp2, cmp3)
        inss = ins1 + [ins0]
        return tcmp(inss, ttmp)
    if (tm0.ctag == "TMlam"):
        x01 = tm0.arg1
        fun0 = tfun_new()
        arg0 = targ_new()
        cenv = cenv_cons(x01, arg0, cenv)
        cmp1 = term_comp01(tm0.arg3, cenv)
        inss = [tins_fun(fun0, arg0, cmp1)]
        return tcmp(inss, fun0)
    if (tm0.ctag == "TMfix"):
        f00 = tm0.arg1
        x01 = tm0.arg2
        fun0 = tfun_new()
        arg0 = targ_new()
        cenv = cenv_cons(f00, fun0, cenv)
        cenv = cenv_cons(x01, arg0, cenv)
        cmp1 = term_comp01(tm0.arg5, cenv)
        inss = [tins_fun(fun0, arg0, cmp1)]
        return tcmp(inss, fun0)
    raise TypeError(tm0) # HX-2025-06-18: unsupported!

print("comp00(int_1) = " + str(term_comp00(int_1)))
print("comp00(btf_t) = " + str(term_comp00(btf_t)))
print("comp00(term_add(int_1, int_2)) = " + str(term_comp00(term_add(int_1, int_2))))
print("comp00(term_dbl) = " + str(term_comp00(term_dbl)))

##################################################################

# datatype tins =
# | TINSmov of (treg(*dst*), tval(*src*))
# | TINSapp of (treg(*res*), treg(*fun*), treg(*arg*))
# | TINSopr of (treg(*res*), strn(*opr*), list(treg))
# | TINSfun of (treg(*f00*), treg(*x01*), tcmp(*body*))
# | TINSif0 of (treg(*res*), treg(*test*), tcmp(*then*), tcmp(*else*))

def endl_emit():
    strn_emit('\n')

def strn_emit(strn):
    print(strn, end='')

def tval_emit(tval):
    strn_emit(str(tval))

def treg_emit(treg):
    strn_emit(treg.prfx);
    strn_emit(str(treg.sffx));

def nind_emit(nind):
    i0 = 0
    while(i0 < nind):
        i0 = i0 + 1
        strn_emit(' ')
    return None

def topr_emit(opnm):
    if (opnm == "+"):
        strn_emit("TINSadd"); return
    if (opnm == "-"):
        strn_emit("TINSsub"); return
    if (opnm == "*"):
        strn_emit("TINSmul"); return
    if (opnm == "/"):
        strn_emit("TINSdiv"); return
    if (opnm == "%"):
        strn_emit("TINSmod"); return
    if (opnm == "<"):
        strn_emit("TINSilt"); return
    if (opnm == ">"):
        strn_emit("TINSigt"); return
    if (opnm == "<="):
        strn_emit("TINSile"); return
    if (opnm == ">="):
        strn_emit("TINSige"); return
    raise TypeError(opnm) # HX-2025-06-24: unsupported!

def args_emit(args):
    i0 = 0
    n0 = len(args)
    while(i0 < n0):
        if (i0 >= 1):
            strn_emit(', ')
        treg_emit(args[i0])
        i0 = i0 + 1
    return None

def tins_emit(tins, nind):
    # print("tins_emit: tins = (" + str(tins) + ")")
    nind_emit(nind)
    # TINSmov of (treg(*dst*), tval(*src*))
    if (tins.ctag == "TINSmov"):
        treg_emit(tins.arg1); strn_emit(' = '); tval_emit(tins.arg2); endl_emit()
        return
    # TINSapp of (treg(*res*), treg(*fun*), treg(*arg*))
    if (tins.ctag == "TINSapp"):
        treg_emit(tins.arg1); strn_emit(' = ')
        treg_emit(tins.arg2); strn_emit('('); treg_emit(tins.arg3); strn_emit(')'); endl_emit()
        return
    # TINSopr of (treg(*res*), strn(*opr*), list(treg))
    if (tins.ctag == "TINSopr"):
        treg_emit(tins.arg1); strn_emit(' = ')
        topr_emit(tins.arg2); strn_emit('('); args_emit(tins.arg3); strn_emit(')'); endl_emit()
        return
    # TINSfun of (treg(*f00*), treg(*x01*), tcmp(*body*))
    if (tins.ctag == "TINSfun"):
        tcmp_body = tins.arg3
        strn_emit('def ')
        treg_emit(tins.arg1); strn_emit('(')
        treg_emit(tins.arg2); strn_emit('):'); endl_emit()
        tinslst_emit(tcmp_body.arg1, nind+2)
        nind_emit(nind+2)
        strn_emit('return '); treg_emit(tcmp_body.arg2); endl_emit()
        return
    # TINSif0 of (treg(*res*), treg(*test*), tcmp(*then*), tcmp(*else*))
    if (tins.ctag == "TINSif0"):
        tcmp_then = tins.arg3
        tcmp_else = tins.arg4
        treg_emit(tins.arg1); strn_emit(' = '); strn_emit('None'); endl_emit()
        nind_emit(nind)
        strn_emit('if ('); treg_emit(tins.arg2); strn_emit('):');  endl_emit()
        tinslst_emit(tcmp_then.arg1, nind+2)
        nind_emit(nind+2)
        treg_emit(tins.arg1); strn_emit(' = '); treg_emit(tcmp_then.arg2); endl_emit()
        nind_emit(nind); strn_emit('else:'); endl_emit()
        tinslst_emit(tcmp_else.arg1, nind+2)
        nind_emit(nind+2)
        treg_emit(tins.arg1); strn_emit(' = '); treg_emit(tcmp_else.arg2); endl_emit()
        return
    # HX: please finish the rest of the cases
    raise TypeError(tins) # HX-2025-06-24: should be deadcode!    

def tinslst_emit(inss, nind):
    for tins in inss: tins_emit(tins, nind)

##################################################################

nind = 0
tcmp_fact = term_comp00(term_fact)
tinslst_emit(tcmp_fact.arg1, nind)
tcmp_fact2 = term_comp00(term_fact2)
tinslst_emit(tcmp_fact2.arg1, nind)

##################################################################
# end of [CS391-2025-Summer/lectures/lecture-06-24/lambda3.py]
##################################################################
