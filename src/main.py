from models.basic_schelling_model import BasicSchellingModel
from models.stabilizer_schelling_model import StabilizerSchellingModel
from models.stabilizer_schelling_model_with_costs import (
    StabilizerSchellingModelWithCost,
)


def main():
    print("Schelling's Segreation Model")

    basic_schellilng_model = BasicSchellingModel()
    stabilizer_schelling_model = StabilizerSchellingModel()
    stabilizer_schelling_model_cost = StabilizerSchellingModelWithCost()

    # basic_schellilng_model.run()
    # stabilizer_schelling_model.run()
    stabilizer_schelling_model_cost.run()


if __name__ == "__main__":
    main()
