package com.makemathgreatagain

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
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
import kotlinx.coroutines.launch
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

private val MmgaColors = lightColorScheme(
    primary = Color(0xFF315CA8),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFE7EEF9),
    onPrimaryContainer = Color(0xFF173765),
    secondary = Color(0xFF17756B),
    secondaryContainer = Color(0xFFE1F3EF),
    tertiary = Color(0xFF9A5B10),
    tertiaryContainer = Color(0xFFFFE9C2),
    background = Color(0xFFF5F6F8),
    surface = Color.White,
    surfaceVariant = Color(0xFFE7EAF0),
    onSurface = Color(0xFF1D2430),
    onSurfaceVariant = Color(0xFF5C6472),
    outline = Color(0xFFD6DAE2),
    error = Color(0xFFB42318),
)

private val ScreenPadding = 18.dp
private val CardShape = RoundedCornerShape(8.dp)
private val PillShape = RoundedCornerShape(999.dp)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
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

private enum class TopicFilter(val label: String) {
    All("全部"),
    Open("待补"),
    Mastered("已理解"),
}

private enum class MainTab(val label: String) {
    Knowledge("知识"),
    Path("路线"),
    Review("复习"),
}

@Composable
private fun MmgaApp() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var state by remember { mutableStateOf(UiState(mastered = loadMastered(context))) }

    suspend fun loadTopics() {
        val selectedId = state.selected?.id
        state = state.copy(loading = true, error = null)
        state = try {
            val topics = fetchTopics()
            state.copy(
                loading = false,
                topics = topics,
                selected = selectedId?.let { id -> topics.firstOrNull { it.id == id } },
                error = null,
            )
        } catch (error: Exception) {
            state.copy(loading = false, error = error.message ?: "Request failed")
        }
    }

    LaunchedEffect(Unit) {
        loadTopics()
    }

    MaterialTheme(colorScheme = MmgaColors) {
        Surface(color = MaterialTheme.colorScheme.background) {
            AppScreen(
                state = state,
                onReload = { scope.launch { loadTopics() } },
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
                },
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
    var selectedTab by rememberSaveable { mutableStateOf(MainTab.Knowledge) }

    BackHandler(enabled = state.selected != null, onBack = onBack)
    BackHandler(enabled = state.selected == null && selectedTab != MainTab.Knowledge) {
        selectedTab = MainTab.Knowledge
    }

    Scaffold(
        contentWindowInsets = WindowInsets.safeDrawing,
        topBar = {
            TopAppBar(
                title = { Text("MMGA", fontWeight = FontWeight.SemiBold) },
                navigationIcon = {
                    if (state.selected != null) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.Filled.ArrowBack, contentDescription = "返回")
                        }
                    }
                },
                actions = {
                    IconButton(onClick = onReload, enabled = !state.loading) {
                        Icon(Icons.Filled.Refresh, contentDescription = "刷新")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onSurface,
                    actionIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    navigationIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                ),
            )
        },
        bottomBar = {
            NavigationBar(
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 0.dp,
            ) {
                MainTab.entries.forEach { tab ->
                    NavigationBarItem(
                        selected = selectedTab == tab && state.selected == null,
                        onClick = {
                            if (state.selected != null) onBack()
                            selectedTab = tab
                        },
                        icon = { TabIcon(tab) },
                        label = { Text(tab.label) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant,
                        ),
                    )
                }
            }
        },
    ) { padding ->
        if (state.selected != null) {
            TopicDetail(
                topic = state.selected,
                topics = state.topics,
                mastered = state.mastered,
                answer = state.answer,
                onToggleMastered = onToggleMastered,
                onAsk = onAsk,
                modifier = Modifier.padding(padding),
            )
        } else {
            when (selectedTab) {
                MainTab.Knowledge -> TopicList(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Path -> PathScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Review -> ReviewScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )
            }
        }
    }
}

@Composable
private fun TabIcon(tab: MainTab) {
    when (tab) {
        MainTab.Knowledge -> Icon(Icons.Filled.Search, contentDescription = null)
        MainTab.Path -> RouteGlyph()
        MainTab.Review -> ReviewGlyph()
    }
}

@Composable
private fun RouteGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Box(
            modifier = Modifier
                .size(6.dp)
                .clip(CircleShape)
                .background(contentColor),
        )
        Box(
            modifier = Modifier
                .width(2.dp)
                .height(8.dp)
                .background(contentColor.copy(alpha = 0.65f)),
        )
        Box(
            modifier = Modifier
                .size(6.dp)
                .clip(CircleShape)
                .background(contentColor),
        )
    }
}

@Composable
private fun ReviewGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        repeat(3) {
            Box(
                modifier = Modifier
                    .padding(vertical = 2.dp)
                    .width(16.dp)
                    .height(2.dp)
                    .background(contentColor),
            )
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicList(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    var query by rememberSaveable { mutableStateOf("") }
    var filter by rememberSaveable { mutableStateOf(TopicFilter.All) }
    val filteredTopics = state.topics.filter { topic ->
        val matchesQuery = query.trim().isBlank() ||
            listOf(topic.name, topic.grade, topic.human).any {
                it.contains(query.trim(), ignoreCase = true)
            }
        val matchesFilter = when (filter) {
            TopicFilter.All -> true
            TopicFilter.Open -> topic.id !in state.mastered
            TopicFilter.Mastered -> topic.id in state.mastered
        }
        matchesQuery && matchesFilter
    }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            ProgressStrip(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        item {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("搜索知识点") },
                leadingIcon = {
                    Icon(Icons.Filled.Search, contentDescription = null)
                },
                shape = CardShape,
            )
        }
        item {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                TopicFilter.entries.forEach { option ->
                    FilterChip(
                        selected = filter == option,
                        onClick = { filter = option },
                        label = { Text(option.label) },
                    )
                }
            }
        }
        if (state.error != null) {
            item {
                ErrorPanel(message = state.error, onReload = onReload)
            }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) {
                LoadingTopicRow()
            }
        } else if (filteredTopics.isEmpty()) {
            item {
                EmptyPanel()
            }
        } else {
            items(filteredTopics, key = { it.id }) { topic ->
                TopicRow(topic = topic, mastered = topic.id in state.mastered) {
                    onSelect(topic)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun PathScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val groups = state.topics.groupBy { topic -> topic.grade.ifBlank { "未分级" } }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            ProgressStrip(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) { LoadingTopicRow() }
        } else if (groups.isEmpty()) {
            item { EmptyPanel("暂无路线数据") }
        } else {
            groups.forEach { (grade, topics) ->
                item {
                    SectionHeader(
                        title = grade,
                        meta = "${topics.count { it.id in state.mastered }}/${topics.size} 已理解",
                    )
                }
                items(topics, key = { "path-${it.id}" }) { topic ->
                    TopicRow(topic = topic, mastered = topic.id in state.mastered) {
                        onSelect(topic)
                    }
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun ReviewScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val knownIds = state.topics.map { it.id }.toSet()
    val openTopics = state.topics.filter { it.id !in state.mastered }
    val readyTopics = openTopics.filter { topic ->
        topic.prerequisites
            .filter { prerequisite -> prerequisite in knownIds }
            .all { prerequisite -> prerequisite in state.mastered }
    }
    val nextTopics = (readyTopics.ifEmpty { openTopics }).take(8)
    val masteredTopics = state.topics.filter { it.id in state.mastered }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            ProgressStrip(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) { LoadingTopicRow() }
        } else {
            item {
                SectionHeader(
                    title = "下一步",
                    meta = if (nextTopics.isEmpty()) {
                        "没有待补知识点"
                    } else {
                        "${nextTopics.size} 个可继续知识点"
                    },
                )
            }
            if (nextTopics.isEmpty()) {
                item { EmptyPanel("暂无待补知识点") }
            } else {
                items(nextTopics, key = { "next-${it.id}" }) { topic ->
                    TopicRow(topic = topic, mastered = false) {
                        onSelect(topic)
                    }
                }
            }

            item {
                SectionHeader(
                    title = "已理解",
                    meta = "${masteredTopics.size} 个知识点",
                )
            }
            if (masteredTopics.isEmpty()) {
                item { EmptyPanel("还没有已理解记录") }
            } else {
                items(masteredTopics, key = { "review-${it.id}" }) { topic ->
                    TopicRow(topic = topic, mastered = true) {
                        onSelect(topic)
                    }
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun SectionHeader(
    title: String,
    meta: String,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 2.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Bottom,
    ) {
        Text(
            title,
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 18.sp,
            fontWeight = FontWeight.SemiBold,
        )
        Text(
            meta,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun ProgressStrip(
    total: Int,
    mastered: Int,
    loading: Boolean,
) {
    val open = (total - mastered).coerceAtLeast(0)
    val progress = if (total == 0) 0f else mastered.toFloat() / total.toFloat()

    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBlock(
                    label = if (loading) "同步中" else "全部",
                    value = total.toString(),
                    modifier = Modifier.weight(1f),
                )
                MetricBlock(
                    label = "已理解",
                    value = mastered.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.secondary,
                )
                MetricBlock(
                    label = "待补",
                    value = open.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.tertiary,
                )
            }
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(PillShape)
                    .background(MaterialTheme.colorScheme.surfaceVariant),
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(progress.coerceIn(0f, 1f))
                        .height(8.dp)
                        .background(MaterialTheme.colorScheme.primary),
                )
            }
        }
    }
}

@Composable
private fun MetricBlock(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
    valueColor: Color = MaterialTheme.colorScheme.onSurface,
) {
    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Text(
            label,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
        Text(value, color = valueColor, fontSize = 24.sp, fontWeight = FontWeight.SemiBold)
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicRow(
    topic: Topic,
    mastered: Boolean,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier
                .clickable(onClick = onClick)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        topic.name.ifBlank { topic.id },
                        fontSize = 18.sp,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        topic.human.ifBlank { topic.why },
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 14.sp,
                        lineHeight = 20.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
                StatusPill(mastered = mastered)
            }
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                if (topic.grade.isNotBlank()) SmallTag(topic.grade)
                SmallTag("${topic.prerequisites.size} 前置")
                SmallTag("${topic.next.size} 后续")
            }
        }
    }
}

@Composable
private fun StatusPill(mastered: Boolean) {
    val container = if (mastered) {
        MaterialTheme.colorScheme.secondaryContainer
    } else {
        MaterialTheme.colorScheme.tertiaryContainer
    }
    val content = if (mastered) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.tertiary
    val label = if (mastered) "已理解" else "待补"

    Surface(
        shape = PillShape,
        color = container,
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Box(
                modifier = Modifier
                    .size(7.dp)
                    .clip(CircleShape)
                    .background(content),
            )
            Text(label, color = content, fontSize = 12.sp, fontWeight = FontWeight.Medium)
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
    var question by rememberSaveable(topic.id) { mutableStateOf("") }
    var asking by remember(topic.id) { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            DetailHeader(
                topic = topic,
                mastered = topic.id in mastered,
                onToggleMastered = { onToggleMastered(topic) },
            )
        }
        item {
            LearningMap(
                topic = topic,
                topics = topics,
                mastered = mastered,
            )
        }
        item {
            DetailPanel(title = "为什么需要") {
                BodyText(topic.why.ifBlank { "暂无" })
            }
        }
        item {
            DetailPanel(title = "术语") {
                if (topic.terms.isEmpty()) {
                    BodyText("暂无")
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        topic.terms.entries.forEach { entry ->
                            TermRow(term = entry.key, explanation = entry.value)
                        }
                    }
                }
            }
        }
        item {
            DetailPanel(title = "理解路线") {
                if (topic.route.isEmpty()) {
                    BodyText("暂无")
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        topic.route.forEachIndexed { index, value ->
                            RouteStep(index = index + 1, value = value)
                        }
                    }
                }
            }
        }
        item {
            DetailPanel(title = "提问") {
                OutlinedTextField(
                    value = question,
                    onValueChange = { question = it },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    label = { Text("问题") },
                    enabled = !asking,
                    shape = CardShape,
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End,
                ) {
                    Button(
                        onClick = {
                            val submitted = question.trim()
                            if (submitted.isNotEmpty()) {
                                scope.launch {
                                    asking = true
                                    onAsk(topic, submitted)
                                    asking = false
                                }
                            }
                        },
                        enabled = question.isNotBlank() && !asking,
                        shape = CardShape,
                    ) {
                        if (asking) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                color = MaterialTheme.colorScheme.onPrimary,
                                strokeWidth = 2.dp,
                            )
                            Spacer(Modifier.width(8.dp))
                        }
                        Text("发送")
                    }
                }
                if (answer.isNotBlank()) {
                    AnswerBubble(answer = answer)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun DetailHeader(
    topic: Topic,
    mastered: Boolean,
    onToggleMastered: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.Top,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        topic.name.ifBlank { topic.id },
                        fontSize = 26.sp,
                        lineHeight = 32.sp,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        topic.human,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 15.sp,
                        lineHeight = 22.sp,
                    )
                }
                if (topic.grade.isNotBlank()) SmallTag(topic.grade)
            }
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                StatusPill(mastered = mastered)
                Button(onClick = onToggleMastered, shape = CardShape) {
                    Text(if (mastered) "取消已理解" else "标记已理解")
                }
            }
        }
    }
}

@Composable
private fun LearningMap(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
) {
    DetailPanel(title = "知识地图") {
        MapRow("已理解前置", topic.prerequisites.names(topics, onlyMastered = mastered))
        MapRow("待补前置", topic.prerequisites.names(topics, excludeMastered = mastered))
        MapRow("后续知识", topic.next.names(topics))
    }
}

@Composable
private fun DetailPanel(
    title: String,
    content: @Composable ColumnScope.() -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                title,
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
            )
            content()
        }
    }
}

@Composable
private fun MapRow(label: String, value: String) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(label, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(value, fontSize = 15.sp, lineHeight = 22.sp, color = MaterialTheme.colorScheme.onSurface)
    }
}

@Composable
private fun TermRow(term: String, explanation: String) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(term, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        BodyText(explanation)
    }
}

@Composable
private fun RouteStep(index: Int, value: String) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Box(
            modifier = Modifier
                .size(28.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center,
        ) {
            Text(index.toString(), color = MaterialTheme.colorScheme.primary, fontSize = 12.sp)
        }
        BodyText(value, modifier = Modifier.weight(1f))
    }
}

@Composable
private fun AnswerBubble(answer: String) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.secondaryContainer,
    ) {
        Text(
            answer,
            modifier = Modifier.padding(14.dp),
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 15.sp,
            lineHeight = 23.sp,
        )
    }
}

@Composable
private fun BodyText(
    value: String,
    modifier: Modifier = Modifier,
) {
    Text(
        value,
        modifier = modifier,
        color = MaterialTheme.colorScheme.onSurface,
        fontSize = 15.sp,
        lineHeight = 23.sp,
    )
}

@Composable
private fun SmallTag(value: String) {
    Surface(
        shape = PillShape,
        color = MaterialTheme.colorScheme.surfaceVariant,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Text(
            value,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun ErrorPanel(
    message: String,
    onReload: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = Color(0xFFFFF1F0),
        border = BorderStroke(1.dp, Color(0xFFFFDAD6)),
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("加载失败", color = Color(0xFFB42318), fontWeight = FontWeight.SemiBold)
                Text(message, color = Color(0xFF8C1D18), fontSize = 13.sp, maxLines = 2)
            }
            Button(onClick = onReload, shape = CardShape) {
                Text("重试")
            }
        }
    }
}

@Composable
private fun EmptyPanel(message: String = "没有匹配结果") {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Text(
            message,
            modifier = Modifier.padding(18.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun LoadingTopicRow() {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            LoadingBar(width = 0.42f, height = 18.dp)
            LoadingBar(width = 0.88f, height = 14.dp)
            LoadingBar(width = 0.55f, height = 14.dp)
        }
    }
}

@Composable
private fun LoadingBar(width: Float, height: androidx.compose.ui.unit.Dp) {
    Box(
        modifier = Modifier
            .fillMaxWidth(width)
            .height(height)
            .clip(PillShape)
            .background(MaterialTheme.colorScheme.surfaceVariant),
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
        .toSet()

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
