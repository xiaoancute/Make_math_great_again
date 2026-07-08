package com.makemathgreatagain;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Insets;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.WindowInsets;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public final class MainActivity extends Activity {
    private static final String PREFS = "math_learning";
    private static final String MASTERED_TOPICS = "mastered_topics";

    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private final Set<String> masteredIds = new HashSet<>();
    private JSONArray topics = new JSONArray();
    private LinearLayout content;
    private TextView statusView;
    private TextView teacherResultView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            getWindow().setDecorFitsSystemWindows(false);
        }

        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(24), dp(24), dp(24), dp(24));

        ScrollView root = new ScrollView(this);
        root.setBackgroundColor(getColor(R.color.background));
        root.addView(content);
        applySystemBarPadding(root, content);
        setContentView(root);

        loadMastered();
        renderHome();
        loadTopics();
    }

    @Override
    protected void onDestroy() {
        executor.shutdownNow();
        super.onDestroy();
    }

    private void renderHome() {
        content.removeAllViews();
        content.addView(hero());

        Button reload = new Button(this);
        reload.setText("刷新知识点");
        reload.setAllCaps(false);
        reload.setOnClickListener(view -> {
            renderHome();
            loadTopics();
        });
        content.addView(reload);

        statusView = text("正在加载知识点...", 14, R.color.text_secondary, false);
        content.addView(statusView);
    }

    private void loadTopics() {
        statusView.setText("正在连接后端...");
        executor.execute(() -> {
            try {
                JSONArray loadedTopics = new JSONArray(fetch("/topics"));
                mainHandler.post(() -> renderTopics(loadedTopics));
            } catch (IOException | JSONException error) {
                mainHandler.post(() -> {
                    statusView.setText("后端不可用，已切到离线示例");
                    renderTopics(fallbackTopics());
                });
            }
        });
    }

    private void renderTopics(JSONArray loadedTopics) {
        topics = loadedTopics;
        statusView.setText(
                "知识点 " + topics.length() + " 个 · 已理解 " + masteredIds.size() + " 个"
        );
        if (topics.length() == 0) {
            content.addView(section("暂无知识点", "后端还没有返回知识点。"));
            return;
        }

        for (int index = 0; index < topics.length(); index++) {
            try {
                JSONObject topic = topics.getJSONObject(index);
                content.addView(topicCard(topic));
            } catch (JSONException ignored) {
                statusView.setText("有知识点数据无法解析");
            }
        }
    }

    private View hero() {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setBackground(cardBackground(R.color.surface_soft));
        card.setLayoutParams(bottomMargin());
        card.setPadding(dp(18), dp(18), dp(18), dp(4));
        card.addView(text("数学要讲明白", 28, R.color.text_primary, true));
        card.addView(text(
                "先理解概念，再进入术语和公式。",
                16,
                R.color.text_secondary,
                false
        ));
        card.addView(text(
                "当前版本：知识图谱 + 术语解释 + AI 老师",
                14,
                R.color.accent,
                true
        ));
        return card;
    }

    private View topicCard(JSONObject topic) throws JSONException {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setBackground(cardBackground(R.color.surface));
        card.setPadding(dp(16), dp(14), dp(16), dp(14));
        card.setLayoutParams(bottomMargin());
        card.addView(text(topic.getString("name"), 18, R.color.text_primary, true));
        card.addView(text(
                topic.getString("human_explanation"),
                15,
                R.color.text_secondary,
                false
        ));
        if (isMastered(topic)) {
            card.addView(text("已理解", 13, R.color.accent, true));
        }
        card.addView(text(
                "学段：" + topic.optString("grade_band", "unknown") + " · 点开看路线",
                13,
                R.color.accent,
                true
        ));
        card.setOnClickListener(view -> renderTopic(topic));
        return card;
    }

    private void renderTopic(JSONObject topic) {
        try {
            content.removeAllViews();
            Button back = new Button(this);
            back.setText("返回知识点");
            back.setAllCaps(false);
            back.setOnClickListener(view -> {
                renderHome();
                loadTopics();
            });
            content.addView(back);

            content.addView(text(topic.getString("name"), 26, R.color.text_primary, true));
            content.addView(masteryButton(topic));
            content.addView(knowledgeMap(topic));
            content.addView(section("人话解释", topic.getString("human_explanation")));
            content.addView(section("为什么要学", topic.getString("why_needed")));
            content.addView(section(
                    "术语解释",
                    terms(topic.getJSONObject("term_explanations"))
            ));
            content.addView(section(
                    "理解路线",
                    list(topic.getJSONArray("understanding_route"))
            ));
            content.addView(teacherSection(topic));
        } catch (JSONException error) {
            renderHome();
            statusView.setText("知识点数据无法解析: " + error.getMessage());
        }
    }

    private View teacherSection(JSONObject topic) throws JSONException {
        LinearLayout box = card();
        box.addView(text("问 AI 老师", 14, R.color.accent, true));

        EditText question = new EditText(this);
        question.setSingleLine(false);
        question.setMinLines(2);
        question.setHint("例如：这个东西为什么存在？");
        question.setTextColor(getColor(R.color.text_primary));
        question.setHintTextColor(getColor(R.color.text_secondary));
        box.addView(question);

        Button ask = new Button(this);
        ask.setText("让老师讲一遍");
        ask.setAllCaps(false);
        box.addView(ask);

        teacherResultView = text(
                "AI 老师会先讲直觉，再解释术语。",
                15,
                R.color.text_secondary,
                false
        );
        box.addView(teacherResultView);
        ask.setOnClickListener(view ->
                askTeacher(topic, question.getText().toString())
        );
        return box;
    }

    private View masteryButton(JSONObject topic) throws JSONException {
        Button button = new Button(this);
        button.setAllCaps(false);
        button.setText(isMastered(topic) ? "取消已理解" : "标记为已理解");
        button.setOnClickListener(view -> {
            String id = topic.optString("id");
            if (masteredIds.contains(id)) {
                masteredIds.remove(id);
            } else {
                masteredIds.add(id);
            }
            saveMastered();
            renderTopic(topic);
        });
        return button;
    }

    private View knowledgeMap(JSONObject topic) throws JSONException {
        JSONArray prerequisites = topic.getJSONArray("prerequisite_ids");
        JSONArray next = topic.getJSONArray("next_ids");
        String mastered = names(prerequisites, true);
        String weak = names(prerequisites, false);
        String future = names(next, null);
        return section(
                "我的知识地图",
                "已理解前置： " + empty(mastered) + "\n"
                        + "需要补： " + empty(weak) + "\n"
                        + "之后会用到： " + empty(future)
        );
    }

    private void askTeacher(JSONObject topic, String rawQuestion) {
        String question = rawQuestion.trim().isEmpty()
                ? "这个东西为什么存在？"
                : rawQuestion.trim();
        teacherResultView.setText("正在生成...");
        executor.execute(() -> {
            try {
                String query = URLEncoder.encode(question, StandardCharsets.UTF_8.name());
                String path = "/topics/"
                        + topic.optString("id")
                        + "/teacher-answer?age=12&question="
                        + query;
                JSONObject response = new JSONObject(fetch(path));
                mainHandler.post(() -> teacherResultView.setText(response.optString("answer")));
            } catch (IOException | JSONException error) {
                mainHandler.post(() ->
                        teacherResultView.setText(localTeacherAnswer(topic, question))
                );
            }
        });
    }

    private String localTeacherAnswer(JSONObject topic, String question) {
        return "你问的是：" + question + "\n\n"
                + "先用人话说：" + topic.optString("human_explanation") + "\n\n"
                + "为什么要学它：" + topic.optString("why_needed") + "\n\n"
                + "先按这条路理解：\n"
                + listQuietly(topic.optJSONArray("understanding_route")) + "\n\n"
                + "如果还卡住，先说清楚：是哪个词不懂，还是哪一步不懂？";
    }

    private String listQuietly(JSONArray items) {
        if (items == null) {
            return "暂无";
        }
        try {
            return list(items);
        } catch (JSONException ignored) {
            return "暂无";
        }
    }

    private boolean isMastered(JSONObject topic) {
        return masteredIds.contains(topic.optString("id"));
    }

    private String names(JSONArray ids, Boolean masteredOnly) throws JSONException {
        StringBuilder text = new StringBuilder();
        for (int index = 0; index < ids.length(); index++) {
            String id = ids.getString(index);
            boolean mastered = masteredIds.contains(id);
            if (masteredOnly != null && masteredOnly != mastered) {
                continue;
            }
            if (text.length() > 0) {
                text.append("、");
            }
            text.append(topicName(id));
        }
        return text.toString();
    }

    private String topicName(String id) {
        for (int index = 0; index < topics.length(); index++) {
            JSONObject topic = topics.optJSONObject(index);
            if (topic != null && id.equals(topic.optString("id"))) {
                return topic.optString("name", id);
            }
        }
        return id;
    }

    private String empty(String value) {
        return value.isEmpty() ? "暂无" : value;
    }

    private void loadMastered() {
        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        masteredIds.clear();
        masteredIds.addAll(prefs.getStringSet(MASTERED_TOPICS, new HashSet<>()));
    }

    private void saveMastered() {
        getSharedPreferences(PREFS, MODE_PRIVATE)
                .edit()
                .putStringSet(MASTERED_TOPICS, new HashSet<>(masteredIds))
                .apply();
    }

    private View section(String title, String body) {
        LinearLayout box = card();
        box.addView(text(title, 14, R.color.accent, true));
        box.addView(text(
                body.isEmpty() ? "暂无" : body,
                16,
                R.color.text_primary,
                false
        ));
        return box;
    }

    private String terms(JSONObject terms) throws JSONException {
        StringBuilder text = new StringBuilder();
        Iterator<String> keys = terms.keys();
        while (keys.hasNext()) {
            String key = keys.next();
            text.append(key).append(": ").append(terms.getString(key)).append("\n");
        }
        return text.toString().trim();
    }

    private String list(JSONArray items) throws JSONException {
        StringBuilder text = new StringBuilder();
        for (int index = 0; index < items.length(); index++) {
            text.append(index + 1).append(". ").append(items.getString(index)).append("\n");
        }
        return text.toString().trim();
    }

    private String fetch(String path) throws IOException {
        HttpURLConnection connection = null;
        try {
            URL url = new URL(getString(R.string.api_base_url) + path);
            connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(3000);
            connection.setReadTimeout(3000);
            connection.setRequestMethod("GET");
            if (connection.getResponseCode() >= 400) {
                throw new IOException("HTTP " + connection.getResponseCode());
            }
            return readBody(connection);
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    private JSONArray fallbackTopics() {
        JSONArray fallback = new JSONArray();
        try {
            fallback.put(new JSONObject()
                    .put("id", "function_intro")
                    .put("name", "函数入门")
                    .put("grade_band", "junior")
                    .put(
                            "human_explanation",
                            "函数是在描述一个量变了，另一个量怎样跟着变。"
                    )
                    .put(
                            "why_needed",
                            "函数能用来预测、画图和推理变化。"
                    )
                    .put("prerequisite_ids", new JSONArray()
                            .put("quantity_relationship"))
                    .put("next_ids", new JSONArray())
                    .put("term_explanations", new JSONObject()
                            .put("变量", "会变化的数量。")
                            .put("输入", "先给进去的那个数或条件。")
                            .put("输出", "根据输入得到的结果。"))
                    .put("understanding_route", new JSONArray()
                            .put("生活变化")
                            .put("两个量之间关系")
                            .put("输入输出")
                            .put("表格")
                            .put("图像")
                            .put("函数表达式")));
            fallback.put(new JSONObject()
                    .put("id", "quantity_relationship")
                    .put("name", "数量关系")
                    .put("grade_band", "primary_to_junior")
                    .put(
                            "human_explanation",
                            "数量关系是在说几个数量怎样互相影响。"
                    )
                    .put(
                            "why_needed",
                            "方程、函数和应用题都从发现数量关系开始。"
                    )
                    .put("prerequisite_ids", new JSONArray())
                    .put("next_ids", new JSONArray().put("function_intro"))
                    .put("term_explanations", new JSONObject()
                            .put("数量", "可以数出来或量出来的多少。")
                            .put("关系", "几个数量互相影响的方式。"))
                    .put("understanding_route", new JSONArray()
                            .put("生活变化")
                            .put("两个量")
                            .put("影响关系")
                            .put("表达关系")));
        } catch (JSONException ignored) {
            return new JSONArray();
        }
        return fallback;
    }

    private String readBody(HttpURLConnection connection) throws IOException {
        InputStream stream = connection.getInputStream();
        try (
                BufferedReader reader = new BufferedReader(
                        new InputStreamReader(stream, StandardCharsets.UTF_8)
                )
        ) {
            StringBuilder body = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                body.append(line);
            }
            return body.toString();
        }
    }

    private TextView text(String value, int sp, int color, boolean bold) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextColor(getColor(color));
        view.setTextSize(sp);
        view.setPadding(0, 0, 0, dp(16));
        if (bold) {
            view.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        }
        return view;
    }

    private LinearLayout card() {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setBackground(cardBackground(R.color.surface));
        box.setLayoutParams(bottomMargin());
        box.setPadding(dp(16), dp(14), dp(16), dp(2));
        return box;
    }

    private GradientDrawable cardBackground(int color) {
        GradientDrawable background = new GradientDrawable();
        background.setColor(getColor(color));
        background.setCornerRadius(dp(8));
        background.setStroke(dp(1), getColor(R.color.border));
        return background;
    }

    private LinearLayout.LayoutParams bottomMargin() {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        params.setMargins(0, 0, 0, dp(12));
        return params;
    }

    private void applySystemBarPadding(View root, View target) {
        int base = dp(24);
        root.setOnApplyWindowInsetsListener((view, insets) -> {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                Insets bars = insets.getInsets(WindowInsets.Type.systemBars());
                target.setPadding(
                        base + bars.left,
                        base + bars.top,
                        base + bars.right,
                        base + bars.bottom
                );
                return insets;
            }

            target.setPadding(
                    base + insets.getSystemWindowInsetLeft(),
                    base + insets.getSystemWindowInsetTop(),
                    base + insets.getSystemWindowInsetRight(),
                    base + insets.getSystemWindowInsetBottom()
            );
            return insets;
        });
        root.requestApplyInsets();
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
