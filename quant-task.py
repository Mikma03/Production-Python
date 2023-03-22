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
