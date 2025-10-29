import matplotlib.pyplot as plt
from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.simple_virtual_liquidity_pool import SimpleVirtualLiquidityPool
from source.purchase_generators.seignorage_model_random_purchase_generator import SeignorageModelRandomPurchaseGenerator
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.reference_token import ReferenceToken
from source.simulations.three_pools_simulation import ThreePoolsSimulation


try:
    number_of_iterations = 2000

    stablecoin_initial_price = 1.0
    stablecoin_initial_supply = 10 ** 6
    stablecoin_initial_free_supply = 10 ** 6 * 0.5
    stablecoin_pool_fee = 0.0

    collateral_initial_price = 15.0
    collateral_initial_supply = 10 ** 6
    collateral_initial_free_supply = 10 ** 6 * 0.5
    collateral_pool_fee = 0.0

    vlp_stablecoin_base_quantity = 10 ** 5
    vlp_pool_fee = 0.0
    pool_recovery_period = 200

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

    stablecoin_purchase_generator = SeignorageModelRandomPurchaseGenerator(token=stablecoin,
                                                                           volatility_variance=1.0,
                                                                           initial_volatility=100.0,
                                                                           delta_variation=lambda x: 1 / x - 1,
                                                                           threshold=0.05)

    collateral_purchase_generator = SeignorageModelRandomPurchaseGenerator(token=collateral,
                                                                           volatility_variance=1.0,
                                                                           initial_volatility=100.0,
                                                                           delta_variation=lambda x: 1 / x - 1,
                                                                           threshold=0.05)

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
