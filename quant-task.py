from typing import Literal, Union, List
import json


class InitialData:
    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        with open(initial_data, "r") as test_data:
            data = json.load(test_data)
        return data


class Order:
    def __init__(
        self,
        order_type: Literal["Iceberg", "Limit"],
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        self.order_type = order_type
        self.direction = direction
        self.order_id = order_id
        self.price = price
        self.quantity = quantity


class IcebergOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self.peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "peak": self.peak,
        }


class LimitOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class OrderDataFactory:
    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        for data in entry_json_order_data:
            order_data = data["order"]

            if data["type"].lower() == "iceberg":
                Iceberg_order = IcebergOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                    order_data["peak"],
                )
                if Iceberg_order.direction.lower() == "buy":
                    buy_orders[Iceberg_order.order_id] = Iceberg_order
                else:
                    sell_orders[Iceberg_order.order_id] = Iceberg_order

            elif data["type"].lower() == "limit":
                Limit_order = LimitOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                )
                if Limit_order.direction.lower() == "buy":
                    buy_orders[Limit_order.order_id] = Limit_order
                else:
                    sell_orders[Limit_order.order_id] = Limit_order

            else:
                raise Exception("Unknown order type")

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        sorted_buy_orders = sorted(
            buy_orders.values(),
            key=lambda order: (-order.price, order.order_id),
        )

        sorted_sell_orders = sorted(
            sell_orders.values(),
            key=lambda order: (order.price, order.order_id),
        )

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        matched_orders = []
        buy_index = 0
        sell_index = 0

        while buy_index < len(buy_orders) and sell_index < len(sell_orders):
            buy_order = buy_orders[buy_index]
            sell_order = sell_orders[sell_index]

            if buy_order.price >= sell_order.price:
                matched_orders.append((buy_order, sell_order))
                buy_index += 1
                sell_index += 1
            else:
                buy_index += 1

        return matched_orders

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        print("\nMatched Orders:")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def subtract_and_display_updated_order_book(
        matched_orders_with_quantity: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ],
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        OrderBook.subtract_matched_amount(matched_orders_with_quantity)
        Executor.display_current_status_of_order_book(buy_orders, sell_orders)

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )
        sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
            buy_orders, sell_orders
        )

        Executor.display_current_status_of_order_book(
            buy_orders=sorted_buy_orders, sell_orders=sorted_sell_orders
        )

        #######################################################################
        print("\n________________FIRST RUN________________")
        #######################################################################

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        #######################################################################
        print("\n________________SECOND RUN________________")
        #######################################################################

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        # Subtract matched amount and display updated order book
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        #######################################################################
        print("________________THIRD RUN________________")
        #######################################################################

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        # Subtract matched amount and display updated order book
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        #######################################################################
        print("________________FOURTH RUN________________")
        #######################################################################

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        # Subtract matched amount and display updated order book
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)



class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        #######################################################################
        print("\n________________FIRST RUN________________")
        #######################################################################

        sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
            buy_orders, sell_orders
        )

        print("\nCurrent status of Order Book")
        print("-------------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=sorted_buy_orders, sell_orders=sorted_sell_orders
        )

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        print("\nUpdated Order Book:")
        print("-------------------------")
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        print("-------------------------")

        (
            cleared_buy_orders_from_first_run,
            cleared_sell_ordersfrom_first_run,
        ) = OrderBook.clear_order_book(sorted_buy_orders, sorted_sell_orders)

        Executor.display_current_status_of_order_book(
            buy_orders=cleared_buy_orders_from_first_run,
            sell_orders=cleared_sell_ordersfrom_first_run,
        )

        #######################################################################
        print("\n________________SECOND RUN________________")
        #######################################################################

        (
            sorted_cleared_buy_orders_from_first_run,
            sorted_cleared_sell_ordersfrom_first_run,
        ) = order_data_factory.sort_orders(
            cleared_buy_orders_from_first_run, cleared_sell_ordersfrom_first_run
        )

        matched_orders = OrderBook.match_orders(
            sorted_cleared_buy_orders_from_first_run,
            sorted_cleared_sell_ordersfrom_first_run,
        )

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        print("\nUpdated Order Book:")
        print("-------------------------")

        # Subtract matched amount and display updated order book
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity,
            sorted_cleared_buy_orders_from_first_run,
            sorted_cleared_sell_ordersfrom_first_run,
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        print("-------------------------")
        (
            sorted_cleared_buy_orders_from_second_run,
            sorted_cleared_sell_ordersfrom_second_run,
        ) = OrderBook.clear_order_book(
            sorted_cleared_buy_orders_from_first_run,
            sorted_cleared_sell_ordersfrom_first_run,
        )

        Executor.display_current_status_of_order_book(
            buy_orders=sorted_cleared_buy_orders_from_second_run,
            sell_orders=sorted_cleared_sell_ordersfrom_second_run,
        )

        #######################################################################
        print("________________THIRD RUN________________")
        #######################################################################

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        # Subtract matched amount and display updated order book
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        #######################################################################
        print("________________FOURTH RUN________________")
        #######################################################################

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )

        matched_orders = OrderBook.match_orders(sorted_buy_orders, sorted_sell_orders)

        matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
            matched_orders
        )

        # Subtract matched amount and display updated order book
        Executor.subtract_and_display_updated_order_book(
            matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
        )

        # Clear the order book and display the updated order book
        print("\nCleared Order Book:")
        Executor.clear_and_display_updated_order_book(
            sorted_buy_orders, sorted_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)




    class OrderBook:
        @staticmethod
        def match_orders(
            buy_orders: list[Union[IcebergOrder, LimitOrder]],
            sell_orders: list[Union[IcebergOrder, LimitOrder]],
        ) -> List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ]:
            matched_orders = []
            buy_index = 0
            sell_index = 0

            while buy_index < len(buy_orders) and sell_index < len(sell_orders):
                buy_order = buy_orders[buy_index]
                sell_order = sell_orders[sell_index]

                if buy_order.price >= sell_order.price:
                    matched_orders.append((buy_order, sell_order))
                    buy_index += 1
                    sell_index += 1
                else:
                    buy_index += 1

            return matched_orders
        



from typing import Literal, Union, List
import json


class InitialData:
    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        with open(initial_data, "r") as test_data:
            data = json.load(test_data)
        return data


class Order:
    def __init__(
        self,
        order_type: Literal["Iceberg", "Limit"],
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        self.order_type = order_type
        self.direction = direction
        self.order_id = order_id
        self.price = price
        self.quantity = quantity


class IcebergOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self.peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "peak": self.peak,
        }


class LimitOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class OrderDataFactory:
    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        for data in entry_json_order_data:
            order_data = data["order"]

            if data["type"].lower() == "iceberg":
                Iceberg_order = IcebergOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                    order_data["peak"],
                )
                if Iceberg_order.direction.lower() == "buy":
                    buy_orders[Iceberg_order.order_id] = Iceberg_order
                else:
                    sell_orders[Iceberg_order.order_id] = Iceberg_order

            elif data["type"].lower() == "limit":
                Limit_order = LimitOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                )
                if Limit_order.direction.lower() == "buy":
                    buy_orders[Limit_order.order_id] = Limit_order
                else:
                    sell_orders[Limit_order.order_id] = Limit_order

            else:
                raise Exception("Unknown order type")

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        sorted_buy_orders = sorted(
            buy_orders.values(),
            key=lambda order: (-order.price, order.order_id),
        )

        sorted_sell_orders = sorted(
            sell_orders.values(),
            key=lambda order: (order.price, order.order_id),
        )

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        matched_orders = []

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if buy_order.price >= sell_order.price:
                    matched_orders.append((buy_order, sell_order))

                    if buy_order.quantity == 0:
                        break
                else:
                    break

        return matched_orders

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        print("\nMatched Orders:")
        print("--------------------")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def subtract_and_display_updated_order_book(
        matched_orders_with_quantity: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ],
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        OrderBook.subtract_matched_amount(matched_orders_with_quantity)
        Executor.display_current_status_of_order_book(buy_orders, sell_orders)

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        while True:
            sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
                buy_orders, sell_orders
            )

            matched_orders = OrderBook.match_orders(
                sorted_buy_orders, sorted_sell_orders
            )

            if not matched_orders:
                break

            matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
                matched_orders
            )

            any_match_with_zero = any(
                matched_quantity == 0
                for _, _, matched_quantity in matched_orders_with_quantity
            )

            if any_match_with_zero:
                break

            Executor.subtract_and_display_updated_order_book(
                matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
            )

            cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            buy_orders = {order.order_id: order for order in cleaned_buy_orders}
            sell_orders = {order.order_id: order for order in cleaned_sell_orders}

        print("\nFinal Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=cleaned_buy_orders, sell_orders=cleaned_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)




###### very close:




from typing import Literal, Union, List
import json


class InitialData:
    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        with open(initial_data, "r") as test_data:
            data = json.load(test_data)
        return data


class Order:
    def __init__(
        self,
        order_type: Literal["Iceberg", "Limit"],
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        self.order_type = order_type
        self.direction = direction
        self.order_id = order_id
        self.price = price
        self.quantity = quantity


class IcebergOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self.peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "peak": self.peak,
        }


class LimitOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class OrderDataFactory:
    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        for data in entry_json_order_data:
            order_data = data["order"]

            if data["type"].lower() == "iceberg":
                Iceberg_order = IcebergOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                    order_data["peak"],
                )
                if Iceberg_order.direction.lower() == "buy":
                    buy_orders[Iceberg_order.order_id] = Iceberg_order
                else:
                    sell_orders[Iceberg_order.order_id] = Iceberg_order

            elif data["type"].lower() == "limit":
                Limit_order = LimitOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                )
                if Limit_order.direction.lower() == "buy":
                    buy_orders[Limit_order.order_id] = Limit_order
                else:
                    sell_orders[Limit_order.order_id] = Limit_order

            else:
                raise Exception("Unknown order type")

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        sorted_buy_orders = sorted(
            buy_orders.values(),
            key=lambda order: (-order.price, order.order_id),
        )

        sorted_sell_orders = sorted(
            sell_orders.values(),
            key=lambda order: (order.price, order.order_id),
        )

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    # @staticmethod
    # def match_orders(
    #     buy_orders: list[Union[IcebergOrder, LimitOrder]],
    #     sell_orders: list[Union[IcebergOrder, LimitOrder]],
    # ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
    #     matched_orders = []

    #     for buy_order in buy_orders:
    #         for sell_order in sell_orders:
    #             if buy_order.price >= sell_order.price:
    #                 matched_orders.append((buy_order, sell_order))

    #                 if buy_order.quantity == 0:
    #                     break
    #             else:
    #                 break

    #     return matched_orders
    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        matched_orders = []

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if buy_order.price >= sell_order.price:
                    matched_quantity = OrderBook.calculate_matched_quantity(
                        buy_order, sell_order
                    )

                    if matched_quantity > 0:
                        matched_orders.append((buy_order, sell_order))

                        buy_order.quantity -= matched_quantity
                        sell_order.quantity -= matched_quantity

                        if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                            buy_order.peak = min(buy_order.peak, buy_order.quantity)

                        if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                            sell_order.peak = min(sell_order.peak, sell_order.quantity)

                    if buy_order.quantity == 0:
                        break
                else:
                    break

        return matched_orders

    @staticmethod
    def update_buy_quantity(
        buy_order: Union[IcebergOrder, LimitOrder], new_quantity: float
    ):
        buy_order.quantity = new_quantity
        if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
            buy_order.peak = min(buy_order.peak, buy_order.quantity)

    @staticmethod
    def update_sell_quantity(
        sell_order: Union[IcebergOrder, LimitOrder], new_quantity: float
    ):
        sell_order.quantity = new_quantity
        if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
            sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        # update_buy_quantity = buy_order.quantity - matched_quantity
        # update_sell_quantity = sell_order.quantity - matched_quantity

        # OrderBook.update_buy_quantity(buy_order, update_buy_quantity)
        # OrderBook.update_sell_quantity(sell_order, update_sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        print("\nMatched Orders:")
        print("--------------------")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def subtract_and_display_updated_order_book(
        matched_orders_with_quantity: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ],
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        OrderBook.subtract_matched_amount(matched_orders_with_quantity)
        Executor.display_current_status_of_order_book(buy_orders, sell_orders)

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        while True:
            sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
                buy_orders, sell_orders
            )

            matched_orders = OrderBook.match_orders(
                sorted_buy_orders, sorted_sell_orders
            )

            if not matched_orders:
                break

            matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
                matched_orders
            )

            any_match_with_zero = any(
                matched_quantity == 0
                for _, _, matched_quantity in matched_orders_with_quantity
            )

            if any_match_with_zero:
                break

            # Executor.subtract_and_display_updated_order_book(
            #     matched_orders_with_quantity, sorted_buy_orders, sorted_sell_orders
            # )
            Executor.display_current_status_of_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            buy_orders = {order.order_id: order for order in cleaned_buy_orders}
            sell_orders = {order.order_id: order for order in cleaned_sell_orders}

        print("\nFinal Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=cleaned_buy_orders, sell_orders=cleaned_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)




# this is almost it:



from typing import Literal, Union, List
import json


class InitialData:
    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        with open(initial_data, "r") as test_data:
            data = json.load(test_data)
        return data


class Order:
    def __init__(
        self,
        order_type: Literal["Iceberg", "Limit"],
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        self.order_type = order_type
        self.direction = direction
        self.order_id = order_id
        self.price = price
        self.quantity = quantity


class IcebergOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self.peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "peak": self.peak,
        }


class LimitOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class OrderDataFactory:
    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        for data in entry_json_order_data:
            order_data = data["order"]

            if data["type"].lower() == "iceberg":
                Iceberg_order = IcebergOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                    order_data["peak"],
                )
                if Iceberg_order.direction.lower() == "buy":
                    buy_orders[Iceberg_order.order_id] = Iceberg_order
                else:
                    sell_orders[Iceberg_order.order_id] = Iceberg_order

            elif data["type"].lower() == "limit":
                Limit_order = LimitOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                )
                if Limit_order.direction.lower() == "buy":
                    buy_orders[Limit_order.order_id] = Limit_order
                else:
                    sell_orders[Limit_order.order_id] = Limit_order

            else:
                raise Exception("Unknown order type")

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        sorted_buy_orders = sorted(
            buy_orders.values(),
            key=lambda order: (-order.price, order.order_id),
        )

        sorted_sell_orders = sorted(
            sell_orders.values(),
            key=lambda order: (order.price, order.order_id),
        )

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        matched_orders = []

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if buy_order.price >= sell_order.price:
                    matched_quantity = OrderBook.calculate_matched_quantity(
                        buy_order, sell_order
                    )

                    if matched_quantity > 0:
                        matched_orders.append((buy_order, sell_order))

                        OrderBook.subtract_matched_amount(
                            [(buy_order, sell_order, matched_quantity)]
                        )

                        if buy_order.quantity == 0:
                            break
                else:
                    break

        return matched_orders

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        print("\nMatched Orders:")
        print("--------------------")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        while True:
            sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
                buy_orders, sell_orders
            )

            matched_orders = OrderBook.match_orders(
                sorted_buy_orders, sorted_sell_orders
            )

            if not matched_orders:
                break

            matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
                matched_orders
            )

            any_match_with_zero = any(
                matched_quantity == 0
                for _, _, matched_quantity in matched_orders_with_quantity
            )

            Executor.display_current_status_of_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            buy_orders = {order.order_id: order for order in cleaned_buy_orders}
            sell_orders = {order.order_id: order for order in cleaned_sell_orders}

            # if any_match_with_zero:
            #     break

        print("\nFinal Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=cleaned_buy_orders, sell_orders=cleaned_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)




##### ALMOST WORKING CODE #####

from typing import Literal, Union, List
import json


class InitialData:
    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        with open(initial_data, "r") as test_data:
            data = json.load(test_data)
        return data


class Order:
    def __init__(
        self,
        order_type: Literal["Iceberg", "Limit"],
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        self.order_type = order_type
        self.direction = direction
        self.order_id = order_id
        self.price = price
        self.quantity = quantity


class IcebergOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self.peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "peak": self.peak,
        }


class LimitOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class OrderDataFactory:
    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        for data in entry_json_order_data:
            order_data = data["order"]

            if data["type"].lower() == "iceberg":
                Iceberg_order = IcebergOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                    order_data["peak"],
                )
                if Iceberg_order.direction.lower() == "buy":
                    buy_orders[Iceberg_order.order_id] = Iceberg_order
                else:
                    sell_orders[Iceberg_order.order_id] = Iceberg_order

            elif data["type"].lower() == "limit":
                Limit_order = LimitOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                )
                if Limit_order.direction.lower() == "buy":
                    buy_orders[Limit_order.order_id] = Limit_order
                else:
                    sell_orders[Limit_order.order_id] = Limit_order

            else:
                raise Exception("Unknown order type")

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        sorted_buy_orders = sorted(
            buy_orders.values(),
            key=lambda order: (-order.price, order.order_id),
        )

        sorted_sell_orders = sorted(
            sell_orders.values(),
            key=lambda order: (order.price, order.order_id),
        )

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        matched_orders = []

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if buy_order.price >= sell_order.price:
                    matched_quantity = OrderBook.calculate_matched_quantity(
                        buy_order, sell_order
                    )

                    if matched_quantity > 0:
                        matched_orders.append((buy_order, sell_order))

                        OrderBook.subtract_matched_amount(
                            [(buy_order, sell_order, matched_quantity)]
                        )

                        if buy_order.quantity == 0:
                            break
                else:
                    break

        return matched_orders

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        print("\nMatched Orders:")
        print("--------------------")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        print("\nInitial status of Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=list(buy_orders.values()), sell_orders=list(sell_orders.values())
        )

        print("\nInitial sorted orders:")
        print("--------------------")
        sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            buy_orders=sorted_buy_orders, sell_orders=sorted_sell_orders
        )

        while True:
            sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
                buy_orders, sell_orders
            )

            matched_orders = OrderBook.match_orders(
                sorted_buy_orders, sorted_sell_orders
            )

            if not matched_orders:
                break

            matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
                matched_orders
            )

            any_match_with_zero = any(
                matched_quantity == 0
                for _, _, matched_quantity in matched_orders_with_quantity
            )

            Executor.display_current_status_of_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            buy_orders = {order.order_id: order for order in cleaned_buy_orders}
            sell_orders = {order.order_id: order for order in cleaned_sell_orders}

            # if any_match_with_zero:
            #     break

        print("\nFinal Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=cleaned_buy_orders, sell_orders=cleaned_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)




#### Final Version of the Code ######


from typing import Literal, Union, List
import json


class InitialData:
    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        with open(initial_data, "r") as test_data:
            data = json.load(test_data)
        return data


class Order:
    def __init__(
        self,
        order_type: Literal["Iceberg", "Limit"],
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        self.order_type = order_type
        self.direction = direction
        self.order_id = order_id
        self.price = price
        self.quantity = quantity


class IcebergOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self.peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "peak": self.peak,
        }


class LimitOrder(Order):
    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class OrderDataFactory:
    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        for data in entry_json_order_data:
            order_data = data["order"]

            if data["type"].lower() == "iceberg":
                Iceberg_order = IcebergOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                    order_data["peak"],
                )
                if Iceberg_order.direction.lower() == "buy":
                    buy_orders[Iceberg_order.order_id] = Iceberg_order
                else:
                    sell_orders[Iceberg_order.order_id] = Iceberg_order

            elif data["type"].lower() == "limit":
                Limit_order = LimitOrder(
                    order_data["direction"],
                    order_data["id"],
                    order_data["price"],
                    order_data["quantity"],
                )
                if Limit_order.direction.lower() == "buy":
                    buy_orders[Limit_order.order_id] = Limit_order
                else:
                    sell_orders[Limit_order.order_id] = Limit_order

            else:
                raise Exception("Unknown order type")

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        sorted_buy_orders = sorted(
            buy_orders.values(),
            key=lambda order: (-order.price, order.order_id),
        )

        sorted_sell_orders = sorted(
            sell_orders.values(),
            key=lambda order: (order.price, order.order_id),
        )

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        matched_orders = []

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if buy_order.price >= sell_order.price:
                    matched_quantity = OrderBook.calculate_matched_quantity(
                        buy_order, sell_order
                    )

                    if matched_quantity > 0:
                        matched_orders.append((buy_order, sell_order))

                        OrderBook.subtract_matched_amount(
                            [(buy_order, sell_order, matched_quantity)]
                        )

                        if buy_order.quantity == 0:
                            break
                else:
                    break

        return matched_orders

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        print("\nMatched Orders:")
        print("--------------------")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    @staticmethod
    def run(json_file: str):
        order_data_factory = OrderDataFactory()

        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        print("\nInitial status of Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=list(buy_orders.values()), sell_orders=list(sell_orders.values())
        )

        print("\nInitial sorted orders:")
        print("--------------------")
        sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            buy_orders=sorted_buy_orders, sell_orders=sorted_sell_orders
        )

        while True:
            sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
                buy_orders, sell_orders
            )

            matched_orders = OrderBook.match_orders(
                sorted_buy_orders, sorted_sell_orders
            )

            if not matched_orders:
                cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                    sorted_buy_orders, sorted_sell_orders
                )
                break

            Executor.display_current_status_of_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
                matched_orders
            )

            cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

            buy_orders = {order.order_id: order for order in cleaned_buy_orders}
            sell_orders = {order.order_id: order for order in cleaned_sell_orders}

        print("\nFinal Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=cleaned_buy_orders, sell_orders=cleaned_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data.json"
    Runner.run(json_file=my_test_json_file)





### FINISH ###

from typing import Literal, Union, List, Callable, Tuple
import json
from pathlib import Path
from functools import total_ordering
from dataclasses import dataclass


class InitialData:
    """
    A class used to read initial data from a JSON file.
    """

    @staticmethod
    def read_json_from_file(initial_data: str) -> List[dict]:
        """
        Read JSON data from the given file.

        Args:
            initial_data (str): The file path of the JSON file to read.

        Returns:
            List[dict]: A list of dictionaries containing the JSON data.
        """

        with Path(initial_data).open("r") as test_data:
            data = json.load(test_data)
        return data


@total_ordering
@dataclass
class Order:
    """
    A class representing a generic order.

    Attributes:
        order_type (Literal["Iceberg", "Limit"]): The type of the order. Must be either "Iceberg" or "Limit".
        direction (Literal["Buy", "Sell"]): The direction of the order. Must be either "Buy" or "Sell".
        order_id (int): The unique identifier of the order.
        price (int): The price of the order.
        quantity (int): The quantity of the order.
    """

    order_type: Literal["Iceberg", "Limit"]
    direction: Literal["Buy", "Sell"]
    order_id: int
    price: int
    quantity: int

    def __post_init__(self):
        if not self.order_type in ("Iceberg", "Limit"):
            raise ValueError("Invalid order_type")
        if not self.direction in ("Buy", "Sell"):
            raise ValueError("Invalid direction")

    def __lt__(self, other):
        if self.direction == other.direction:
            if self.direction == "Buy":
                return self.price < other.price
            else:
                return self.price > other.price
        else:
            return self.direction < other.direction

    def __dict__(self) -> dict[str, Union[str, int]]:
        return {
            "type": self.order_type,
            "direction": self.direction,
            "id": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
        }


class IcebergOrder(Order):
    """
    A class representing an iceberg order, which is a subclass of the Order class.

    Attributes:
        direction (Literal["Buy", "Sell"]): The direction of the order. Must be either "Buy" or "Sell".
        order_id (int): The unique identifier of the order.
        price (float): The price of the order.
        quantity (float): The total quantity of the order.
        peak (float): The visible quantity of the order. Must be greater or equal to zero.
    """

    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
        peak: float,
    ):
        super().__init__("Iceberg", direction, order_id, price, quantity)
        self._peak = peak

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity} {self.peak}"

    @property
    def peak(self):
        return self._peak

    @peak.setter
    def peak(self, value: float):
        if value < 0:
            raise ValueError("Peak value must be greater or equal to zero")
        self._peak = value

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        base_dict = super().__dict__()
        base_dict["peak"] = self.peak
        return base_dict


class LimitOrder(Order):
    """
    A class representing a limit order, which is a subclass of the Order class.

    Attributes:
        direction (Literal["Buy", "Sell"]): The direction of the order. Must be either "Buy" or "Sell".
        order_id (int): The unique identifier of the order.
        price (float): The price of the order.
        quantity (float): The quantity of the order.
    """

    def __init__(
        self,
        direction: Literal["Buy", "Sell"],
        order_id: int,
        price: float,
        quantity: float,
    ):
        super().__init__("Limit", direction, order_id, price, quantity)

    def __repr__(self) -> str:
        return f"{self.order_type} {self.direction} {self.order_id} {self.price} {self.quantity}"

    def __dict__(self) -> dict[str, Union[str, int, float]]:
        return super().__dict__()


class OrderDataFactory:
    """
    A factory class that creates and processes Order objects, specifically IcebergOrder and LimitOrder objects,
    from JSON data.

    This class contains static methods to create Order objects from JSON data, sort buy and sell orders, and
    return sorted lists of buy and sell orders.
    """

    @staticmethod
    def create_order_objects_from_json(
        json_data: str,
    ) -> tuple[
        dict[int, Union[IcebergOrder, LimitOrder]],
        dict[int, Union[IcebergOrder, LimitOrder]],
    ]:
        """
        Create IcebergOrder and LimitOrder objects from JSON data.

        Args:
            json_data (str)

        Returns:
            tuple[dict[int, Union[IcebergOrder, LimitOrder]], dict[int, Union[IcebergOrder, LimitOrder]]]:
            A tuple containing two dictionaries:
                - The first dictionary contains buy orders, where the key is the order_id and the value is the corresponding order object.
                - The second dictionary contains sell orders, where the key is the order_id and the value is the corresponding order object.
        """

        buy_orders = {}
        sell_orders = {}

        entry_json_order_data = InitialData.read_json_from_file(json_data)

        order_mapping: dict[str, Callable[..., Union[IcebergOrder, LimitOrder]]] = {
            "iceberg": IcebergOrder,
            "limit": LimitOrder,
        }

        for data in entry_json_order_data:
            order_type = data["type"].lower()
            order_class = order_mapping.get(order_type)

            if order_class is None:
                raise ValueError(f"Unknown order type: {data['type']}")

            order_data = data["order"]
            order_data["order_id"] = order_data.pop("id")  # Adjust the key name
            order = order_class(**order_data)

            order_dict = buy_orders if order.direction.lower() == "buy" else sell_orders
            order_dict[order.order_id] = order

        return buy_orders, sell_orders

    @staticmethod
    def sort_orders(
        buy_orders: dict[int, Union[IcebergOrder, LimitOrder]],
        sell_orders: dict[int, Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        """
        Sort buy and sell orders based on their price and order_id.

        Args:
            buy_orders (dict[int, Union[IcebergOrder, LimitOrder]]): A dictionary containing buy orders,
                where the key is the order_id and the value is the corresponding order object.
            sell_orders (dict[int, Union[IcebergOrder, LimitOrder]]): A dictionary containing sell orders,
                where the key is the order_id and the value is the corresponding order object.

        Returns:
            tuple[list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]]: A tuple containing two lists:
                - The first list contains sorted buy orders in descending order of price, and ascending order of order_id.
                - The second list contains sorted sell orders in ascending order of price, and ascending order of order_id.
        """

        sort_key: Callable[[Order], tuple] = lambda order: (
            -order.price if order.direction == "Buy" else order.price,
            order.order_id,
        )

        sorted_buy_orders = sorted(buy_orders.values(), key=sort_key)
        sorted_sell_orders = sorted(sell_orders.values(), key=sort_key)

        return sorted_buy_orders, sorted_sell_orders


class OrderBook:
    """
    A class that manages order matching, processing, and clearing of the order book.

    This class contains static methods that handle the matching of buy and sell orders,
    calculation of matched quantities, subtraction of matched quantities, and clearing of the order book.
    """

    @staticmethod
    def match_orders(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
        """
        Match buy and sell orders based on their price.

        Args:
            buy_orders (list[Union[IcebergOrder, LimitOrder]]): A list of buy orders.
            sell_orders (list[Union[IcebergOrder, LimitOrder]]): A list of sell orders.

        Returns:
            List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]:
            A list of tuples containing matched buy and sell orders.
        """

        matched_orders = []

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if buy_order.price >= sell_order.price:
                    matched_quantity = OrderBook.calculate_matched_quantity(
                        buy_order, sell_order
                    )

                    if matched_quantity > 0:
                        matched_orders.append((buy_order, sell_order))

                        OrderBook.subtract_matched_amount(
                            [(buy_order, sell_order, matched_quantity)]
                        )

                        if buy_order.quantity == 0:
                            break
                else:
                    break

            if matched_orders:
                break

        return matched_orders

    @staticmethod
    def calculate_matched_quantity(
        buy_order: Union[IcebergOrder, LimitOrder],
        sell_order: Union[IcebergOrder, LimitOrder],
    ) -> int:
        """
        Calculate the matched quantity between a buy order and a sell order.

        This method takes a buy order and a sell order as arguments and returns the matched quantity between them.
        The matched quantity is the minimum of the available quantity of the buy order and the sell order.
        If either of the orders is an IcebergOrder, the peak value is considered instead of the total quantity.

        Args:
            buy_order (Union[IcebergOrder, LimitOrder]): A buy order, which can be an IcebergOrder or a LimitOrder.
            sell_order (Union[IcebergOrder, LimitOrder]): A sell order, which can be an IcebergOrder or a LimitOrder.

        Returns:
            int: The matched quantity between the buy order and the sell order.
        """

        buy_quantity = (
            buy_order.peak
            if isinstance(buy_order, IcebergOrder)
            else buy_order.quantity
        )
        sell_quantity = (
            sell_order.peak
            if isinstance(sell_order, IcebergOrder)
            else sell_order.quantity
        )
        matched_quantity = min(buy_quantity, sell_quantity)

        return matched_quantity

    @staticmethod
    def subtract_matched_amount(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
        ]
    ):
        """
        Subtract the matched quantities from the buy and sell orders.

        This method takes a list of tuples containing matched buy and sell orders and their matched quantities,
        and subtracts the matched quantities from the orders' available quantities.
        If an order is an IcebergOrder, update its peak value if needed.

        Args:
            matched_orders (List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]]):
            A list of tuples containing matched buy and sell orders and their matched quantities.
        """

        for buy_order, sell_order, matched_quantity in matched_orders:
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity

            if isinstance(buy_order, IcebergOrder) and buy_order.peak > 0:
                buy_order.peak = min(buy_order.peak, buy_order.quantity)

            if isinstance(sell_order, IcebergOrder) and sell_order.peak > 0:
                sell_order.peak = min(sell_order.peak, sell_order.quantity)

    @staticmethod
    def clear_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ) -> tuple[
        list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]
    ]:
        """
        Clear the order book by removing orders with zero quantity.

        This method takes lists of buy and sell orders and returns cleaned lists containing only orders with non-zero quantities.

        Args:
            buy_orders (list[Union[IcebergOrder, LimitOrder]]): A list of buy orders.
            sell_orders (list[Union[IcebergOrder, LimitOrder]]): A list of sell orders.

        Returns:
            tuple[list[Union[IcebergOrder, LimitOrder]], list[Union[IcebergOrder, LimitOrder]]]:
            A tuple containing two lists: cleaned_buy_orders and cleaned_sell_orders.
        """

        cleaned_buy_orders = [order for order in buy_orders if order.quantity != 0]
        cleaned_sell_orders = [order for order in sell_orders if order.quantity != 0]

        return cleaned_buy_orders, cleaned_sell_orders


class Executor:
    """
    A class that manages the display of order book status, matched orders, and the updated order book.

    This class contains static methods that handle displaying the current status of the order book,
    matched orders with their quantities, and the updated order book after clearing orders with zero quantity.
    """

    @staticmethod
    def display_current_status_of_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        """
        Display the current status of the order book.

        This method takes lists of buy and sell orders and prints their details.

        Args:
            buy_orders (list[Union[IcebergOrder, LimitOrder]]): A list of buy orders.
            sell_orders (list[Union[IcebergOrder, LimitOrder]]): A list of sell orders.
        """

        print("\nBuy Orders:")
        for order in buy_orders:
            print(order.__dict__())

        print("\nSell Orders:")
        for order in sell_orders:
            print(order.__dict__())

    @staticmethod
    def display_matched_orders_and_quantity(
        matched_orders: List[
            tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]
        ],
    ) -> List[
        tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]
    ]:
        """
        Display matched orders and their matched quantities.

        This method takes a list of tuples containing matched buy and sell orders and calculates the matched quantities.
        It then prints the matched orders and their matched quantities and returns a list of tuples containing matched orders and quantities.

        Args:
            matched_orders (List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder]]]):
            A list of tuples containing matched buy and sell orders.

        Returns:
            List[tuple[Union[IcebergOrder, LimitOrder], Union[IcebergOrder, LimitOrder], int]]:
            A list of tuples containing matched buy and sell orders and their matched quantities.
        """

        print("\nMatched Orders:")
        print("--------------------")
        matched_orders_with_quantity = []
        for buy_order, sell_order in matched_orders:
            matched_quantity = OrderBook.calculate_matched_quantity(
                buy_order, sell_order
            )
            matched_orders_with_quantity.append(
                (buy_order, sell_order, matched_quantity)
            )
            print(
                f"Buy: {buy_order.__dict__()} <-> Sell: {sell_order.__dict__()} | Matched Quantity: {matched_quantity}"
            )

        return matched_orders_with_quantity

    @staticmethod
    def clear_and_display_updated_order_book(
        buy_orders: list[Union[IcebergOrder, LimitOrder]],
        sell_orders: list[Union[IcebergOrder, LimitOrder]],
    ):
        """
        Clear the order book and display the updated order book.

        This method takes lists of buy and sell orders, clears the orders with zero quantity,
        and displays the updated order book.

        Args:
            buy_orders (list[Union[IcebergOrder, LimitOrder]]): A list of buy orders.
            sell_orders (list[Union[IcebergOrder, LimitOrder]]): A list of sell orders.
        """

        cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
            buy_orders, sell_orders
        )
        Executor.display_current_status_of_order_book(
            cleaned_buy_orders, cleaned_sell_orders
        )


class Runner:
    """
    A class to execute the order book matching process.

    This class contains static methods that run the entire process of reading order data from a JSON file,
    displaying the initial order book status, sorting the orders, matching the orders, clearing the order book,
    and displaying the final order book status.
    """

    @staticmethod
    def run(json_file: str):
        """
        Execute the order book matching process.

        This method takes a JSON file containing order data and runs the order book matching process.
        It displays the initial order book status, sorts the orders, matches the orders, clears the order book,
        and displays the final order book status.

        Args:
            json_file (str): The path to the JSON file containing order data.
        """

        order_data_factory = OrderDataFactory()
        buy_orders, sell_orders = order_data_factory.create_order_objects_from_json(
            json_file
        )

        Runner.display_initial_order_book(buy_orders, sell_orders)
        sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
            buy_orders, sell_orders
        )
        Runner.display_sorted_order_book(sorted_buy_orders, sorted_sell_orders)

        cleaned_buy_orders, cleaned_sell_orders = Runner.process_order_matching(
            buy_orders, sell_orders, order_data_factory
        )

        Runner.display_final_order_book(cleaned_buy_orders, cleaned_sell_orders)

    @staticmethod
    def display_initial_order_book(buy_orders, sell_orders):
        """
        Display the initial order book status.

        Args:
            buy_orders: A dictionary of buy orders.
            sell_orders: A dictionary of sell orders.
        """

        print("\nInitial status of Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=list(buy_orders.values()), sell_orders=list(sell_orders.values())
        )

    @staticmethod
    def display_sorted_order_book(sorted_buy_orders, sorted_sell_orders):
        """
        Display the sorted order book status.

        Args:
            sorted_buy_orders: A list of sorted buy orders.
            sorted_sell_orders: A list of sorted sell orders.
        """

        print("\nInitial sorted orders:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=sorted_buy_orders, sell_orders=sorted_sell_orders
        )

        print("--------------------")
        print("END OF SORTED DATA")
        print("--------------------")

    @staticmethod
    def process_order_matching(buy_orders, sell_orders, order_data_factory):
        """
        Process order matching, clear the order book, and return the cleaned orders.

        Args:
            buy_orders (dict): A dictionary containing buy orders.
            sell_orders (dict): A dictionary containing sell orders.
            order_data_factory (OrderDataFactory): An instance of OrderDataFactory.

        Returns:
            tuple: A tuple containing cleaned_buy_orders and cleaned_sell_orders.
        """

        while True:
            sorted_buy_orders, sorted_sell_orders = order_data_factory.sort_orders(
                buy_orders, sell_orders
            )

            matched_orders = OrderBook.match_orders(
                sorted_buy_orders, sorted_sell_orders
            )

            if not matched_orders:
                cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                    sorted_buy_orders, sorted_sell_orders
                )
                break

            matched_orders_with_quantity = Executor.display_matched_orders_and_quantity(
                matched_orders
            )

            cleaned_buy_orders, cleaned_sell_orders = OrderBook.clear_order_book(
                sorted_buy_orders, sorted_sell_orders
            )

        return cleaned_buy_orders, cleaned_sell_orders

    @staticmethod
    def display_final_order_book(cleaned_buy_orders, cleaned_sell_orders):
        """
        Display the final status of the order book.

        Args:
            cleaned_buy_orders (list): A list of cleaned buy orders.
            cleaned_sell_orders (list): A list of cleaned sell orders.
        """

        print("\nFinal Order Book:")
        print("--------------------")
        Executor.display_current_status_of_order_book(
            buy_orders=cleaned_buy_orders, sell_orders=cleaned_sell_orders
        )


if __name__ == "__main__":
    my_test_json_file = "test_data_2.json"
    Runner.run(json_file=my_test_json_file)
