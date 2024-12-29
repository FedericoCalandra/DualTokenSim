import matplotlib.pyplot as plt
import numpy as np

from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.simple_virtual_liquidity_pool import SimpleVirtualLiquidityPool
from source.purchase_generators.seignorage_model_purchase_generator import SeignorageModelPurchaseGenerator
from source.purchase_generators.seignorage_model_random_purchase_generator import SeignorageModelRandomPurchaseGenerator
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.reference_token import ReferenceToken
from source.simulations.three_pools_simulation import ThreePoolsSimulation


def calculate_volatility_array(volumes_daily, total_iterations_per_day, sqrt_2_pi=0.7979):
    volume_values_daily = [volume / total_iterations_per_day for volume in volumes_daily]
    volume_array = np.repeat(volume_values_daily, total_iterations_per_day)
    volatility_array = volume_array / sqrt_2_pi
    return volatility_array.tolist()


try:
    iterations_per_day = 14400                       # number of blocks produced in 1 day (one every 6 seconds)

    stablecoin_initial_price = 0.9997794183
    stablecoin_initial_supply = 18_490_738_908
    stablecoin_initial_free_supply = stablecoin_initial_supply * 0.5
    stablecoin_pool_fee = 0.03

    collateral_initial_price = 78.34409302
    collateral_initial_supply = 345_341_994.7
    collateral_initial_free_supply = collateral_initial_supply * 0.5
    collateral_pool_fee = 0.03

    vlp_stablecoin_base_quantity = 6.7215e7
    vlp_pool_fee = 0.0
    pool_recovery_period = 36

    volumes_daily_stablecoin = [
        547686207.2, 566644084.6, 574239250.7, 453049346.2, 612280606.5, 733858936.5,
        649583067.2, 1335178681, 2025913193, 2809970941, 4905955011, 7679819164,
        9392162783, 1285921756, 376460753.5, 335182961.8, 389081589.1, 264405278.3,
        173247622.4, 102877376.6, 59116608.94, 45170671.07, 78643834.72, 90652769.19,
        59529498.26, 174553602.3, 117938242.9, 27457467.57, 21456925.2, 14038645.96,
        32885587.67
    ]
    volumes_daily_collateral = [
        1712121334, 1788318413, 1955818800, 1302497178, 1941974963, 2276428168,
        2178573977, 3054299674, 5108105142, 6306976142, 10452679386, 11564567908,
        15924391896, 1900824923, 8213042862, 4009983321, 3319818663, 1530284129,
        872930871.1, 645836243.7, 371474667, 541297631.1, 2070375662, 1148270980,
        550617442.6, 904717263.3, 279589030, 90453864.15, 120807443.9, 79442977.19,
        353589189
    ]

    number_of_iterations = iterations_per_day * len(volumes_daily_collateral)

    volatility_array_stablecoin = calculate_volatility_array(volumes_daily_stablecoin, iterations_per_day)
    volatility_array_collateral = calculate_volatility_array(volumes_daily_collateral, iterations_per_day)

    print(len(volatility_array_stablecoin))
    print(len(volatility_array_collateral))

    cpf = ConstantProductFormula()

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

    stablecoin_pool_quantity = stablecoin_initial_supply - stablecoin_initial_free_supply
    stablecoin_pool_reference_quantity = stablecoin_pool_quantity * stablecoin_initial_price

    collateral_pool_quantity = collateral_initial_supply - collateral_initial_free_supply
    collateral_pool_reference_quantity = collateral_pool_quantity * collateral_initial_price

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
                                              fee=vlp_pool_fee,
                                              pool_recovery_period=int(pool_recovery_period))

    stablecoin_purchase_generator = SeignorageModelPurchaseGenerator(token=stablecoin,
                                                                     volatility=volatility_array_stablecoin,
                                                                     delta_variation=lambda x: 1 / x - 1,
                                                                     threshold=0.05,
                                                                     pool_fee=stablecoin_pool_fee)

    collateral_purchase_generator = SeignorageModelPurchaseGenerator(token=collateral,
                                                                     volatility=volatility_array_collateral,
                                                                     delta_variation=lambda x: 1 / x - 1,
                                                                     threshold=0.05,
                                                                     pool_fee=collateral_pool_fee)

    simulation = ThreePoolsSimulation(stablecoin_token=stablecoin,
                                      collateral_token=collateral,
                                      reference_token=reference,
                                      stablecoin_pool=stablecoin_pool,
                                      collateral_pool=collateral_pool,
                                      virtual_pool=virtual_pool,
                                      stablecoin_purchase_generator=stablecoin_purchase_generator,
                                      collateral_purchase_generator=collateral_purchase_generator,
                                      number_of_iterations=number_of_iterations)

    print("Running Simulation...")
    results = simulation.run_simulation()

    # Plot Results
    print("Simulation Complete. Displaying Results...")

    # Stablecoin and Collateral Prices
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    plt.plot(results["stablecoin_price_history"], label="Stablecoin Price", color="blue")
    plt.title("Stablecoin Price History")
    plt.xlabel("Iterations")
    plt.ylabel("Price")
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(results["collateral_price_history"], label="Collateral Price", color="orange")
    plt.title("Collateral Price History")
    plt.xlabel("Iterations")
    plt.ylabel("Price")
    plt.legend()

    # Supplies
    plt.subplot(2, 2, 3)
    plt.plot(results["stablecoin_supply_history"], label="Stablecoin Supply", color="blue")
    plt.plot(results["collateral_supply_history"], label="Collateral Supply", color="orange")
    plt.title("Token Supply History")
    plt.xlabel("Iterations")
    plt.ylabel("Supply")
    plt.legend()

    # Virtual Pool Delta
    plt.subplot(2, 2, 4)
    plt.plot(results["virtual_pool_delta"], label="Virtual Pool Delta", color="green")
    plt.title("Virtual Pool Delta")
    plt.xlabel("Iterations")
    plt.ylabel("Delta")
    plt.legend()

    plt.tight_layout()
    plt.show()

except ValueError as e:
    print(f"Error: {e}")
