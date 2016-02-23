"""
Cookie Clicker Simulator
"""

import clicker 
import math
import simpleplot


SIM_TIME = 10000000000.0


BUILD_GROWTH = 1.15

class BuildInfo:
    """
    Class to track build information.
    """
    
    def __init__(self, build_info = None, growth_factor = BUILD_GROWTH):
        self._build_growth = growth_factor
        if build_info == None:
            self._info = {"Cursor": [15.0, 0.1],
                          "Grandma": [100.0, 0.5],
                          "Farm": [500.0, 4.0],
                          "Factory": [3000.0, 10.0],
                          "Mine": [10000.0, 40.0],
                          "Shipment": [40000.0, 100.0],
                          "Alchemy Lab": [200000.0, 400.0],
                          "Portal": [1666666.0, 6666.0],
                          "Time Machine": [123456789.0, 98765.0],
                          "Antimatter Condenser": [3999999999.0, 999999.0]}
        else:
            self._info = {}
            for key, value in build_info.items():
                self._info[key] = list(value)
            
    def build_items(self):
        """
        Get a list of buildable items
        """
        return self._info.keys()
            
    def get_cost(self, item):
        """
        Get the current cost of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][0]
    
    def get_cps(self, item):
        """
        Get the current CPS of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][1]
    
    def update_item(self, item):
        """
        Update the cost of an item by the growth factor
        Will throw a KeyError exception if item is not in the build info.
        """
        cost, cps = self._info[item]
        self._info[item] = [cost * self._build_growth, cps]
        
    def clone(self):
        """
        Return a clone of this BuildInfo
        """
        return BuildInfo(self._info, self._build_growth)

    
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies_ = 0.0          # should be a float
        self._total_cookies_ = 0.0    # total cookies earned so far
        self._cps_ = 1.0              
        self._current_time_ = 0.0     
        self._history_ = [(0.0, None, 0.0, 0.0)]  
        
    def __str__(self):
        """
        Return human readable state
        """
        return \
            "Time: " + str(self._current_time_)  + \
            " Current cookies: " + str(self._cookies_) + \
            " CPS: " + str(self._cps_) + \
            " Total cookies: " + str(self._total_cookies_) 
            
            
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies_ 
    
    def get_cps(self):
        """
        Get current CPS
        Should return a float
        """
        return self._cps_ 
    
    def get_time(self):
        """
        Get current time
        Should return a float
        """
        return self._current_time_ 
    
    def get_history(self):
        """
        Return history list
        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)
        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history_ 

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)
        Should return a float with no fractional part
        """
        if self._cookies_ >= cookies: 
            return 0.0
        else:
            return math.ceil((cookies - self._cookies_)/self._cps_) 
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0
        """
        if time <= 0:   
            return

        self._cookies_ = self._cookies_ + time * self._cps_               # update cookies
        self._total_cookies_ = self._total_cookies_ + time * self._cps_   # update total cookies
        self._current_time_ += time                                   # update time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        if self._cookies_ >= cost:
            self._cookies_ -= cost
            self._cps_ += additional_cps
            self._history_.append( (self._current_time_, item_name, cost, self._total_cookies_) )
        else:
            return

        
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    click_object = ClickerState()           # create a click state object
    build_info_object = build_info.clone()  # create a clone of build_info

   
    # 1:
    # Check the current time and break out of the loop 
    # if the duration has been passed
    while click_object.get_time() <= duration:
       
        # 2:
        # Call the strategy function with the appropriate arguments to determine 
        # which item to purchase next. If the strategy function returns None, 
        # you should break out of the loop, as that means no more items 
        # will be purchased.
        time_left = duration - click_object.get_time()
        item = strategy( click_object.get_cookies(), click_object.get_cps(), 
             time_left, build_info_object ) 
        if item is None:
            break

        # 3:
        # Determine how much time must elapse until it is possible to purchase the item. 
        # If you would have to wait past the duration of the simulation 
        # to purchase the item, you should end the simulation.
        
        # 4:
        # Wait until that time.
        cost = build_info_object.get_cost(item)
        time_to_wait = click_object.time_until(cost)    # only wait to integer
        if time_left < time_to_wait:
            break
        else:
            click_object.wait(time_to_wait)

        # 5.
        # Buy the item
        click_object.buy_item(item, cost, build_info_object.get_cps(item) )
        
        # 6.
        # Update the build information.
        build_info_object.update_item(item)
    
    # Wait the amount of time left:
    time_left = duration - click_object.get_time()
    if time_left > 0:
        click_object.wait( time_left)
         

    return click_object          


def strategy_cursor_broken(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None
    
def map_costs_to_items():
    available_items = build_info.build_items()
    item_costs = {}
    for item in available_items:
        cost = build_info.get_cost(item)
        item_costs[cost] = item
        costs.append(cost)
    return item_costs

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    future_cookies = cookies + cps * time_left
    costs_map = map_costs_to_items()
    return costs_mapping[min(filter(lambda x: x <= future_cookies, 
                                    costs_map.keys()))]


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    future_cookies = cookies + cps * time_left
    costs_map = map_costs_to_items()
    return costs_mapping[max(filter(lambda x: x <= future_cookies, 
                                    costs_map.keys()))]


def strategy_best(cookies, cps, time_left, build_info):
    """
    Best strategy to earn the most total cookies with the default SIM_TIME
    """
    item = strategy_best_cps_cost_ratio( cookies, cps, time_left, build_info )
    return item 


def strategy_best_cps_cost_ratio( cookies, cps, time_left, build_info):
    """
    From the affordable item list, choose the one with the best cps/cost ratio
    """
    end_cookies = cookies + cps * time_left
    item_list = build_info.build_items()

    best_ratio_item = None
    best_ratio = 0.0
    for item in item_list:
        if build_info.get_cost( item ) > end_cookies:
            continue
       
        # if no item has been choosed, choose this one 
        if best_ratio_item == None:
            best_ratio_item = item
            best_ratio = build_info.get_cps( item )/ build_info.get_cost( item)
            continue
        
        curr_ratio = build_info.get_cps(item)/build_info.get_cost(item)

        if  curr_ratio > best_ratio: 
            best_ratio = curr_ratio
            best_ratio_item = item

    return best_ratio_item
        

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(clicker.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

