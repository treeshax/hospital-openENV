from env.hospital_env import HospitalEnv
import random


# 🎯 Simple baseline agent (random actions)
def random_agent_action():
    departments = ["cardiology", "neurology", "orthopedics", "general"]
    seriousness_levels = [1, 2, 3, 4, 5]

    return {
        "department": random.choice(departments),
        "seriousness": random.choice(seriousness_levels)
    }


def run_episode(env):
    state = env.reset()
    done = False

    total_reward = 0
    step_num = 1

    while not done:
        # 🩺 INPUT STATE
        print(f"\n🩺 Step {step_num}")
        print("INPUT STATE:")
        print(f"Symptoms: {state['symptoms']}")
        print(f"Age: {state['age']}")
        print(f"Heart Rate: {state['heart_rate']}")
        print(f"Blood Pressure: {state['blood_pressure']}")

        # 🤖 AGENT ACTION
        action = random_agent_action()
        print("\nAGENT ACTION:")
        print(f"Department: {action['department']}")
        print(f"Seriousness: {action['seriousness']}")

        # 🚀 ENV STEP
        next_state, reward, done, info = env.step(action)

        # 🎯 OUTPUT
        print(f"\nREWARD: {reward}")
        print(f"TRUE DEPARTMENT: {info['true_department']}")
        print(f"TRUE SERIOUSNESS: {info['true_seriousness']}")
        print(f"RUNNING ACCURACY: {info['accuracy']:.2f}")
        print("-" * 40)

        total_reward += reward
        state = next_state
        step_num += 1

    return total_reward, info["accuracy"]


if __name__ == "__main__":

    # 🔥 Choose difficulty
    TASK = "easy"   # change to "medium" or "hard"

    # ✅ FIXED (no data=None)
    env = HospitalEnv(task=TASK, max_steps=20)

    EPISODES = 1  # keep 1 for clean output

    for ep in range(EPISODES):
        total_reward, accuracy = run_episode(env)

        print(f"\n📊 Episode {ep+1} Summary")
        print(f"Total Reward: {total_reward}")
        print(f"Final Accuracy: {accuracy:.2f}")
        print("=" * 50)