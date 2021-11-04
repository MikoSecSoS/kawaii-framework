
class CaseDict(dict):
    """
    不区分大小写的字典
    使用两个字典来存放数据
    1个存放名称,一个存数据
    """
    def __init__(self,**kw):
        """__init__(self,**kw)"""
        self.kp = {};
        for k in kw.keys():
            self.__setitem__(k,kw[k]);
    
    def __contains__(self, k):
        """__contains__(self, k)"""
        if isinstance(k,str):
            kn=k.lower();
            if not self.kp.__contains__(kn):
                return False;
            k=kn;
        return super().__contains__(k);
        
    def __setitem__(self,k,v):
        """__setitem__(self,k,v)"""
        if isinstance(k,str):
            kn=k.lower();
            self.kp[kn]=k;
            k=kn;
        super().__setitem__(k,v);
    
    def  __delitem__(self,k):
        """ __delitem__(self,k)"""
        if isinstance(k,str):
            k=k.lower();
            self.kp.pop(k);
        super.__delitem__(k);
    
    def __getitem__(self, k):
        """__getitem__(self, k)"""
        if isinstance(k,str):
            k=k.lower();
        return super().__getitem__(k);
    
    def actual_key_case(self, k):
        """actual_key_case(self, k) 获取真实的key名"""
        if isinstance(k,str):
            return self.kp[k.lower()];
        return k;