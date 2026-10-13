class Item():
  def __init__(self ,name,item_id,brand,color,location,date,description,item_type,status):
    self.set_name(name)
    self.set_brand(brand)
    self.set_color(color)
    self.set_location(location)
    self.set_date(date)
    self.set_description(description)
    self.set_type(item_type)
    self.set_status(status)
    self.set_item_id(item_id)


  def set_name(self,name):
    if isinstance(name,str) and len(name) > 0:
      self.__name=name
    else :
      raise ValueError

  def get_name(self):
    return self.__name

  def set_brand(self,brand):
    if isinstance(brand,str) and len(brand) > 0:
      self.__brand=brand
    else :
      raise ValueError

  def get_brand(self):
    return self.__brand

  def set_color(self,color):
    if isinstance(color,str) and len(color) > 0:
      self.__color=color
    else :
      raise ValueError

  def get_color(self):
    return self.__color

  
  def set_location(self,location):
    if isinstance(location,str) and len(location) > 0:
      self.__location=location
    else :
      raise ValueError

  def get_location(self):
    return self.__location


  def set_date(self,date):
    if isinstance(date,str) and len(date) > 0:
      self.__date=date
    else :
      raise ValueError

  def get_date(self):
    return self.__date

  def set_description(self,description):
    if isinstance(description,str):
      self.__description=description
    else :
      raise ValueError

  def get_description(self):
    return self.__description


  def set_type(self,item_type):
    if isinstance(item_type,str) and item_type in('lost','found'):
       self.__item_type=item_type
    else :
      raise ValueError

  def get_type(self):
    return self.__item_type

  def set_status(self,status):
    if isinstance(status,str) and status in('active','resolved'):
      self.__status=status
    else :
      raise ValueError

  def get_status(self):
    return self.__status

  def set_item_id(self,item_id):
    if isinstance(item_id,str)  and len(item_id) > 0:
      self.__item_id=item_id
    else :
      raise ValueError

  def get_item_id(self):
    return self.__item_id

 
  def display_info(self):
    return {
        "Item ID": self.get_item_id(),
        "Name": self.get_name(),
        "Brand": self.get_brand(),
        "Color": self.get_color(),
        "Location": self.get_location(),
        "Date": self.get_date(),
        "Description": self.get_description(),
        "Type": self.get_type(),
        "Status": self.get_status()
    }
    
    
    
class LostItem(Item):
      def __init__(self ,name,item_id,brand,color,location,date,description,item_type,status,reward):
          super().__init__(name, item_id, brand, color, location, date, description, item_type, status)
          self.set_reward(reward)
  
      def set_reward(self,reward):
            if isinstance(reward,(int,float))  :
                self.__reward=reward
            else :
                raise ValueError

      def get_reward(self):
            return self.__reward

      def display_info(self):
            info = super().display_info()
            info['reward'] = self.get_reward()
            return info
        
        

class FoundItem(Item):
      def __init__(self ,name,item_id,brand,color,location,date,description,item_type,status,storage_loc):
        super().__init__(name, item_id, brand, color, location, date, description, item_type, status)
        self.set_storage_loc(storage_loc)

      def set_storage_loc(self,storage_loc):
        if isinstance(storage_loc,(str))  :
            self.__storage_loc=storage_loc
        else :
            raise ValueError

      def get_storage_loc(self):
        return self.__storage_loc

      def display_info(self):
        info = super().display_info()
        info['storage_loc'] = self.get_storage_loc()
        return info
    
    

class LostFoundSystem:  

  def __init__(self):
    self.__items=[]

  def add_item(self,item):
    if isinstance(item,Item):
      self.__items.append(item)
    else:
      raise ValueError


  def search(self,search_term):
    l=[]
    for i in self.__items:
        if  search_term.lower() in i.get_name().lower():
          l.append(i)
    return l

        
  def remove_item(self,item_id):
    for i in self.__items:
      if item_id.lower()==i.get_item_id().lower():
        self.__items.remove(i)


  def update_status(self,item_id,new_status):
    for i in self.__items:
      if item_id== i.get_item_id():
        i.set_status(new_status)





        
                    
        

    
  



    
