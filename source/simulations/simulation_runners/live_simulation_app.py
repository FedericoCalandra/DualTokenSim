from source.gui.simulation_dashboard.build.gui_dashboard import GUIDashboard
from source.gui.simulation_initialization.build.gui_param_initializer import GUIParamInitializer
from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.simple_virtual_liquidity_pool import SimpleVirtualLiquidityPool
from source.purchase_generators.seignorage_model_purchase_generator import SeignorageModelPurchaseGenerator
from source.purchase_generators.seignorage_model_random_purchase_generator import SeignorageModelRandomPurchaseGenerator
from source.simulations.three_pools_live_simulation import ThreePoolsLiveSimulation
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.reference_token import ReferenceToken
from source.wallets_generators.exponential_wallets_generator import ExponentialWalletsGenerator


def validate_positive_number(value, param_name):
    """
    Ensures the value is a positive number.
    """
    try:
        value = float(value)
        if value < 0:
            raise ValueError(f"{param_name} must be a positive number.")
        return value
    except ValueError:
        raise ValueError(f"{param_name} must be a positive number and numeric.")


def validate_fee(value, param_name):
    """
    Ensures the fee is a number between 0 and 1.
    """
    value = validate_positive_number(value, param_name)
    if not (0 <= value <= 1):
        raise ValueError(f"{param_name} must be between 0 and 1.")
    return value


def validate_supply(free_supply, total_supply):
    """
    Ensures the free supply is less than or equal to the total supply.
    """
    free_supply = validate_positive_number(free_supply, "Free Supply")
    total_supply = validate_positive_number(total_supply, "Total Supply")
    if free_supply > total_supply:
        raise ValueError("Free supply cannot exceed total supply.")
    return free_supply, total_supply


live_simulation = None
initializer = GUIParamInitializer()

try:
    stablecoin_params = initializer.simulation_parameters["stablecoin"]
    collateral_params = initializer.simulation_parameters["collateral_token"]
    vlp_params = initializer.simulation_parameters["virtual_liquidity_pool"]

    stablecoin_initial_price = validate_positive_number(stablecoin_params["price"], "Stablecoin Price")
    stablecoin_initial_free_supply, stablecoin_initial_supply = validate_supply(
        stablecoin_params["free_supply"], stablecoin_params["supply"]
    )
    stablecoin_pool_fee = validate_fee(stablecoin_params["pool_fee"], "Stablecoin Pool Fee")

    collateral_initial_price = validate_positive_number(collateral_params["price"], "Collateral Price")
    collateral_initial_free_supply, collateral_initial_supply = validate_supply(
        collateral_params["free_supply"], collateral_params["supply"]
    )
    collateral_pool_fee = validate_fee(collateral_params["pool_fee"], "Collateral Pool Fee")

    vlp_stablecoin_base_quantity = validate_positive_number(vlp_params["base"], "VLP Base Quantity")
    pool_recovery_period = validate_positive_number(vlp_params["pool_recovery"], "Pool Recovery Period")
    vlp_fee = validate_fee(vlp_params["pool_fee"], "VLP Fee")

    stablecoin_pool_quantity = stablecoin_initial_supply - stablecoin_initial_free_supply
    stablecoin_pool_reference_quantity = stablecoin_pool_quantity * stablecoin_initial_price
    collateral_pool_quantity = collateral_initial_supply - collateral_initial_free_supply
    collateral_pool_reference_quantity = collateral_pool_quantity * collateral_initial_price

    cpf = ConstantProductFormula()

    stablecoin_max_wallet_probability = 0.001
    collateral_max_wallet_probability = 0.001

    swap_volume = 1000.0
    delta_variation = lambda x: 1 / x - 1
    threshold = 0.05

    stablecoin = AlgorithmicStablecoin(name="AS",
                                       peg=1.0,
                                       initial_price=stablecoin_initial_price,
                                       initial_supply=stablecoin_initial_supply,
                                       initial_free_supply=stablecoin_initial_free_supply)

    collateral = CollateralToken(name="CT",
                                 initial_price=collateral_initial_price,
                                 initial_supply=collateral_initial_supply,
                                 initial_free_supply=collateral_initial_free_supply,
                                 algorithmic_stablecoin=stablecoin)

    reference = ReferenceToken(name="USD")

    stablecoin_pool = LiquidityPool(token_a=stablecoin,
                                    token_b=reference,
                                    quantity_token_a=stablecoin_pool_quantity,
                                    quantity_token_b=stablecoin_pool_reference_quantity,
                                    formula=cpf,
                                    fee=stablecoin_pool_fee)

    collateral_pool = LiquidityPool(token_a=collateral,
                                    token_b=reference,
                                    quantity_token_a=collateral_pool_quantity,
                                    quantity_token_b=collateral_pool_reference_quantity,
                                    formula=cpf,
                                    fee=collateral_pool_fee)

    virtual_pool = SimpleVirtualLiquidityPool(stablecoin=stablecoin,
                                              collateral=collateral,
                                              stablecoin_base_quantity=vlp_stablecoin_base_quantity,
                                              formula=cpf,
                                              fee=vlp_fee,
                                              pool_recovery_period=int(pool_recovery_period))

    stablecoin_wallets_generator = ExponentialWalletsGenerator(
        probability_associated_to_total_free_token=stablecoin_max_wallet_probability)

    collateral_wallets_generator = ExponentialWalletsGenerator(
        probability_associated_to_total_free_token=stablecoin_max_wallet_probability)

    stablecoin_purchase_generator = SeignorageModelRandomPurchaseGenerator(token=stablecoin,
                                                                           wallets_generator=stablecoin_wallets_generator,
                                                                           volatility_variance=swap_volume,
                                                                           delta_variation=delta_variation,
                                                                           threshold=threshold)
    collateral_purchase_generator = SeignorageModelRandomPurchaseGenerator(token=collateral,
                                                                           wallets_generator=collateral_wallets_generator,
                                                                           volatility_variance=swap_volume,
                                                                           delta_variation=delta_variation,
                                                                           threshold=threshold)

    live_simulation = ThreePoolsLiveSimulation(stablecoin_token=stablecoin,
                                               collateral_token=collateral,
                                               reference_token=reference,
                                               stablecoin_pool=stablecoin_pool,
                                               collateral_pool=collateral_pool,
                                               virtual_pool=virtual_pool,
                                               stablecoin_purchase_generator=stablecoin_purchase_generator,
                                               collateral_purchase_generator=collateral_purchase_generator)

except ValueError as e:
    print(f"Parameter Validation Error: {e}")

if live_simulation is not None:
    dashboard = GUIDashboard(live_simulation)
