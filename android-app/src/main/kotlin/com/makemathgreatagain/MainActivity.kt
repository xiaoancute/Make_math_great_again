package com.makemathgreatagain

import android.app.Activity
import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.nio.charset.StandardCharsets

private const val PREFS = "math_learning"
private const val MASTERED_TOPICS = "mastered_topics"
private const val API_BASE_URL = "http://10.0.2.2:8000"

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MmgaApp() }
    }
}

private data class Topic(
    val id: String,
    val name: String,
    val grade: String,
    val human: String,
    val why: String,
    val prerequisites: List<String>,
    val next: List<String>,
    val terms: Map<String, String>,
    val route: List<String>,
)

private data class UiState(
    val loading: Boolean = true,
    val error: String? = null,
    val topics: List<Topic> = emptyList(),
    val selected: Topic? = null,
    val mastered: Set<String> = emptySet(),
    val answer: String = "",
)

@Composable
private fun MmgaApp() {
    val context = LocalContext.current
    var state by remember { mutableStateOf(UiState(mastered = loadMastered(context))) }

    LaunchedEffect(Unit) {
        state = try {
            state.copy(loading = false, topics = fetchTopics(), error = null)
        } catch (error: Exception) {
            state.copy(loading = false, error = error.message ?: "Request failed")
        }
    }

    MaterialTheme(
        colorScheme = MaterialTheme.colorScheme.copy(
            primary = Color(0xFF2563EB),
            surface = Color.White,
            background = Color(0xFFF7F8FA),
        )
    ) {
        Surface(color = MaterialTheme.colorScheme.background) {
            AppScreen(
                state = state,
                onReload = {
                    state = state.copy(loading = true, error = null, selected = null)
                    (context as Activity).recreate()
                },
                onSelect = { state = state.copy(selected = it, answer = "") },
                onBack = { state = state.copy(selected = null, answer = "") },
                onToggleMastered = { topic ->
                    val mastered = state.mastered.toMutableSet()
                    if (!mastered.add(topic.id)) mastered.remove(topic.id)
                    saveMastered(context, mastered)
                    state = state.copy(mastered = mastered)
                },
                onAsk = { topic, question ->
                    state = state.copy(answer = "加载中")
                    state = try {
                        state.copy(answer = fetchTeacherAnswer(topic.id, question))
                    } catch (_: Exception) {
                        state.copy(answer = "请求失败")
                    }
                }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun AppScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    onBack: () -> Unit,
    onToggleMastered: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("MMGA", fontWeight = FontWeight.SemiBold) },
                actions = {
                    if (state.selected == null) {
                        TextButton(onClick = onReload) { Text("刷新") }
                    } else {
                        TextButton(onClick = onBack) { Text("返回") }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        }
    ) { padding ->
        if (state.selected == null) {
            TopicList(
                state = state,
                onSelect = onSelect,
                modifier = Modifier.padding(padding)
            )
        } else {
            TopicDetail(
                topic = state.selected,
                topics = state.topics,
                mastered = state.mastered,
                answer = state.answer,
                onToggleMastered = onToggleMastered,
                onAsk = onAsk,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun TopicList(
    state: UiState,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            SummaryCard(
                loading = state.loading,
                error = state.error,
                total = state.topics.size,
                mastered = state.mastered.size,
            )
        }
        items(state.topics) { topic ->
            TopicCard(topic = topic, mastered = topic.id in state.mastered) {
                onSelect(topic)
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun SummaryCard(
    loading: Boolean,
    error: String?,
    total: Int,
    mastered: Int,
) {
    AppCard(container = Color(0xFFEAF2FF)) {
        Text("知识点", fontSize = 14.sp, color = Color(0xFF2563EB))
        Text(
            if (loading) "加载中" else "$total 个 · $mastered 个已理解",
            fontSize = 26.sp,
            fontWeight = FontWeight.Bold
        )
        if (error != null) {
            Text(error, color = Color(0xFFB42318), fontSize = 14.sp)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicCard(
    topic: Topic,
    mastered: Boolean,
    onClick: () -> Unit,
) {
    AppCard(modifier = Modifier.clickable(onClick = onClick)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Column(modifier = Modifier.weight(1f)) {
                Text(topic.name, fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
                Text(
                    topic.human,
                    color = Color(0xFF5B6472),
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            StatusDot(active = mastered)
        }
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (topic.grade.isNotBlank()) Chip(topic.grade)
            if (mastered) Chip("已理解")
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicDetail(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
    answer: String,
    onToggleMastered: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var question by remember(topic.id) { mutableStateOf("") }
    var asking by remember { mutableStateOf(false) }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            AppCard(container = Color(0xFFEAF2FF)) {
                Text(topic.name, fontSize = 28.sp, fontWeight = FontWeight.Bold)
                Text(topic.human, color = Color(0xFF435064))
                Button(onClick = { onToggleMastered(topic) }) {
                    Text(if (topic.id in mastered) "取消已理解" else "标记为已理解")
                }
            }
        }
        item {
            Section("知识地图") {
                Text("已理解前置：${topic.prerequisites.names(topics, mastered)}")
                Text("待补前置：${topic.prerequisites.names(topics, null, mastered)}")
                Text("后续知识：${topic.next.names(topics)}")
            }
        }
        item { TextSection("为什么需要", topic.why) }
        item {
            TextSection(
                "术语",
                topic.terms.entries.joinToString("\n") { "${it.key}：${it.value}" }
            )
        }
        item {
            TextSection(
                "理解路线",
                topic.route.mapIndexed { i, value -> "${i + 1}. $value" }.joinToString("\n")
            )
        }
        item {
            Section("提问") {
                OutlinedTextField(
                    value = question,
                    onValueChange = { question = it },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 2,
                    label = { Text("问题") }
                )
                Spacer(Modifier.height(10.dp))
                Button(
                    onClick = {
                        asking = true
                    },
                    enabled = question.isNotBlank()
                ) {
                    Text("发送")
                }
                if (asking) {
                    LaunchedEffect(question, topic.id) {
                        onAsk(topic, question)
                        asking = false
                    }
                }
                if (answer.isNotBlank()) {
                    Spacer(Modifier.height(12.dp))
                    Text(answer, color = Color(0xFF27313F))
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun TextSection(title: String, value: String) {
    Section(title) {
        Text(if (value.isBlank()) "暂无" else value, color = Color(0xFF27313F))
    }
}

@Composable
private fun Section(title: String, content: @Composable () -> Unit) {
    AppCard {
        Text(title, color = Color(0xFF2563EB), fontWeight = FontWeight.SemiBold)
        Spacer(Modifier.height(6.dp))
        content()
    }
}

@Composable
private fun AppCard(
    modifier: Modifier = Modifier,
    container: Color = Color.White,
    content: @Composable Column.() -> Unit,
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = container),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
            content = content
        )
    }
}

@Composable
private fun Chip(value: String) {
    AssistChip(onClick = {}, label = { Text(value) })
}

@Composable
private fun StatusDot(active: Boolean) {
    Box(
        modifier = Modifier
            .size(12.dp)
            .clip(CircleShape)
            .background(if (active) Color(0xFF16A34A) else Color(0xFFCBD5E1))
    )
}

private fun List<String>.names(
    topics: List<Topic>,
    onlyMastered: Set<String>? = null,
    excludeMastered: Set<String>? = null,
): String {
    val names = filter {
        (onlyMastered == null || it in onlyMastered) &&
            (excludeMastered == null || it !in excludeMastered)
    }.map { id -> topics.firstOrNull { it.id == id }?.name ?: id }
    return names.joinToString("、").ifBlank { "暂无" }
}

private suspend fun fetchTopics(): List<Topic> = withContext(Dispatchers.IO) {
    val array = JSONArray(fetch("/topics"))
    List(array.length()) { index -> array.getJSONObject(index).toTopic() }
}

private suspend fun fetchTeacherAnswer(topicId: String, question: String): String =
    withContext(Dispatchers.IO) {
        val query = URLEncoder.encode(question, StandardCharsets.UTF_8.name())
        JSONObject(fetch("/topics/$topicId/teacher-answer?age=12&question=$query"))
            .optString("answer")
    }

private fun JSONObject.toTopic(): Topic = Topic(
    id = optString("id"),
    name = optString("name"),
    grade = optString("grade_band"),
    human = optString("human_explanation"),
    why = optString("why_needed"),
    prerequisites = optJSONArray("prerequisite_ids").toStringList(),
    next = optJSONArray("next_ids").toStringList(),
    terms = optJSONObject("term_explanations").toStringMap(),
    route = optJSONArray("understanding_route").toStringList(),
)

private fun JSONArray?.toStringList(): List<String> {
    if (this == null) return emptyList()
    return List(length()) { index -> optString(index) }
}

private fun JSONObject?.toStringMap(): Map<String, String> {
    if (this == null) return emptyMap()
    return keys().asSequence().associateWith { key -> optString(key) }
}

private fun loadMastered(context: Context): Set<String> =
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getStringSet(MASTERED_TOPICS, emptySet())
        .orEmpty()

private fun saveMastered(context: Context, value: Set<String>) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putStringSet(MASTERED_TOPICS, value)
        .apply()
}

private fun fetch(path: String): String {
    val connection = URL(API_BASE_URL + path).openConnection() as HttpURLConnection
    return try {
        connection.connectTimeout = 3000
        connection.readTimeout = 3000
        connection.requestMethod = "GET"
        if (connection.responseCode >= 400) error("HTTP ${connection.responseCode}")
        connection.inputStream.bufferedReader().use { it.readText() }
    } finally {
        connection.disconnect()
    }
}
