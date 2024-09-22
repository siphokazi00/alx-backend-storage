-- Drop the existing trigger if it exists
DROP TRIGGER IF EXISTS decrease_quantity;

-- Create the trigger that fires after an insert on the orders table
CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity of the item based on the number ordered
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
