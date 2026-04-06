from env.hospital_env import HospitalEnv
import random
from collections import defaultdict

# 🎯 Possible actions
DEPARTMENTS = [
    "cardiology",
    "neurology",
    "orthopedics",
    "general",
    "pulmonology",
    "emergency"
]
SERIOUSNESS = [1, 2, 3, 4, 5]

ACTIONS = [(d, s) for d in DEPARTMENTS for s in SERIOUSNESS]


# 🧠 Q-Table (state-action values)
Q = defaultdict(lambda: [0] * len(ACTIONS))


# 🔑 Convert state → simple key
def state_to_key(state):
    return (
        state["symptoms"],
        state["age"] // 10,          # bucket age
        state["heart_rate"] // 10,   # bucket HR
        state["blood_pressure"] // 10
    )


# 🎯 Choose action (epsilon-greedy)
def choose_action(state, epsilon=0.2):
    key = state_to_key(state)

    if random.random() < epsilon:
        return random.choice(ACTIONS), random.randint(0, len(ACTIONS)-1)

    q_values = Q[key]
    max_idx = q_values.index(max(q_values))
    return ACTIONS[max_idx], max_idx


# 🔁 TRAINING LOOP
def train(env, episodes=500):

    alpha = 0.1
    gamma = 0.95

    epsilon = 1.0          # start fully random
    epsilon_min = 0.05     # minimum exploration
    epsilon_decay = 0.995  # slowly reduce randomness

    for ep in range(episodes):
        state = env.reset()
        done = False

        total_reward = 0

        while not done:
            key = state_to_key(state)

            # 🎯 epsilon-greedy
            if random.random() < epsilon:
                action_idx = random.randint(0, len(ACTIONS)-1)
            else:
                action_idx = Q[key].index(max(Q[key]))

            dept, ser = ACTIONS[action_idx]

            action_dict = {
                "department": dept,
                "seriousness": ser
            }

            next_state, reward, done, info = env.step(action_dict)

            total_reward += reward

            # 🔥 STRONGER LEARNING FROM MISTAKES
            if reward < 0:
                reward *= 1.5   # amplify penalty

            next_key = state_to_key(next_state) if next_state else None
            max_future = max(Q[next_key]) if next_key else 0

            Q[key][action_idx] += alpha * (
                reward + gamma * max_future - Q[key][action_idx]
            )

            state = next_state

        # 📉 reduce randomness
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        print(f"Episode {ep+1} | Reward: {total_reward:.2f} | Accuracy: {info['accuracy']:.2f} | Epsilon: {epsilon:.2f}")


# 🧪 TEST (after training)
def test(env):
    state = env.reset()
    done = False

    while not done:
        key = state_to_key(state)
        q_values = Q[key]
        best_idx = q_values.index(max(q_values))

        dept, ser = ACTIONS[best_idx]

        action = {
            "department": dept,
            "seriousness": ser
        }

        print("\n🩺 INPUT:", state)
        print("🤖 ACTION:", action)

        state, reward, done, info = env.step(action)

        print("🎯 REWARD:", reward)
        print("✅ TRUE:", info["true_department"], info["true_seriousness"])
        print("-" * 40)


if __name__ == "__main__":

    env = HospitalEnv(task="hard", max_steps=20)

    print("🚀 Training started...\n")
    train(env, episodes=200)

    print("\n🧪 Testing trained agent...\n")
    test(env)