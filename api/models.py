from django.db import models


class Product(models.Model):
    #類別屬性
    currency = models.CharField(max_length=255,blank=False, null=False)#字串欄位，長度255字
    cash_buy = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True) # 浮點數 預設值0
    cash_sell = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True) # 浮點數 預設值0
    date = models.DateField()

    class Meta:
        unique_together = ('currency', 'date')

    def __str__(self):
        return f'{self.id}  幣別: {self.currency}  日期: {self.date}  買入: {self.cash_buy} 賣出: {self.cash_sell} '



#
# class Order(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product)
#     # user 是 django 內建資料模型
#     # ForeignKey 代表另一個 model的id
#     # ManyToMany 代表多筆資料
#
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"
