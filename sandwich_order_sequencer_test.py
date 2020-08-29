"""
    Simple test for the Sandwich Sequencer task.
    ! unfortunately the coding took nearly two hours so do not have time to write a test suite ->
      manually (visually) testing the output !
      If I had more time I would have looked at using: https://github.com/spulec/freezegun and intercept std-out.

      @Author: Adam Cripps
"""
from time import sleep
from sandwich_order_sequencer import SandwichShopScheduler


def test():
    scheduler = SandwichShopScheduler()

    # Set the action times shorter for testing.
    scheduler.SEC_TO_MAKE_SANDWICH = 2
    scheduler.SEC_TO_SERVE_SANDWICH = 1

    # Test.
    scheduler.add_order()
    sleep(3)
    scheduler.add_order()
    sleep(4)
    scheduler.add_order()
    scheduler.add_order()
    sleep(6)
    scheduler.add_order()


if __name__ == '__main__':
    test()

"""
    Test Results For Short Times: 
         1. 02:37 Make Sandwich 1
         2. 02:39 Serve Sandwich 1
         3. 02:40 Take a break. 

         1. 02:37 Make Sandwich 1
         2. 02:39 Serve Sandwich 1
         3. 02:40 Make Sandwich 2
         4. 02:42 Serve Sandwich 2
         5. 02:43 Take a break. 

         1. 02:37 Make Sandwich 1
         2. 02:39 Serve Sandwich 1
         3. 02:40 Make Sandwich 2
         4. 02:42 Serve Sandwich 2
         5. 02:43 Take a break. 
         6. 02:44 Make Sandwich 3
         7. 02:46 Serve Sandwich 3
         8. 02:47 Take a break. 

         1. 02:37 Make Sandwich 1
         2. 02:39 Serve Sandwich 1
         3. 02:40 Make Sandwich 2
         4. 02:42 Serve Sandwich 2
         5. 02:43 Take a break. 
         6. 02:44 Make Sandwich 3
         7. 02:46 Serve Sandwich 3
         8. 02:47 Make Sandwich 4
         9. 02:49 Serve Sandwich 4
         10. 02:50 Take a break. 

         1. 02:37 Make Sandwich 1
         2. 02:39 Serve Sandwich 1
         3. 02:40 Make Sandwich 2
         4. 02:42 Serve Sandwich 2
         5. 02:43 Take a break. 
         6. 02:44 Make Sandwich 3
         7. 02:46 Serve Sandwich 3
         8. 02:47 Make Sandwich 4
         9. 02:49 Serve Sandwich 4
         10. 02:50 Make Sandwich 5
         11. 02:52 Serve Sandwich 5
         12. 02:53 Take a break.
"""